from django.shortcuts import render
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, Profile, Comment
from .serializers import UserSerializer, ReviewSerializer, ProfileSerializer, CommentSerializer
from django.contrib.auth.models import User
from .utils import get_movie_details

# View to list and create reviews
class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Adding support for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating']
    search_fields = ['movie_title']
    ordering_fields = ['created_date', 'rating']

    # Fetch movie details when listing reviews
    def get(self, request, *args, **kwargs):
        reviews = self.get_queryset()
        data = []

        for review in reviews:
            movie_details = get_movie_details(review.movie_title)  # Fetch movie details
            review_data = ReviewSerializer(review).data
            review_data['movie_details'] = movie_details  # Add movie details to the response
            data.append(review_data)

        return Response(data)

    # Associate review with the current authenticated user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View for retrieving, updating, and deleting a review
class ReviewDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

# View to create a user
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# View for user details, updates, and deletion
class UserDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# API endpoint for liking and unliking a review
@api_view(['POST'])
def like_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        if request.user in review.likes.all():
            review.likes.remove(request.user)  # Remove like
        else:
            review.likes.add(request.user)  # Add like
        return Response({'likes': review.total_likes()})
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# View to retrieve a user's profile
class UserProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'  # Access profiles by username

# View to create comments on reviews
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = Review.objects.get(pk=self.kwargs['pk'])  # Add error handling here
        serializer.save(user=self.request.user, review=review)

# View for movie recommendations based on user reviews
class MovieRecommendationView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user_reviews = Review.objects.filter(user=self.request.user)
        user_movie_titles = user_reviews.values_list('movie_title', flat=True)
        return Review.objects.exclude(user=self.request.user).filter(movie_title__in=user_movie_titles).distinct()

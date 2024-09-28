from django.urls import path
from .views import (
    ReviewListCreate, 
    ReviewDetailUpdateDelete, 
    UserCreate, 
    UserDetailUpdateDelete, 
    like_review, 
    UserProfileView, 
    CommentCreateView, 
    MovieRecommendationView
)

urlpatterns = [
    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),  # List all reviews or create a new review
    path('reviews/<int:pk>/', ReviewDetailUpdateDelete.as_view(), name='review-detail-update-delete'),  # Retrieve, update, or delete a review
    path('users/', UserCreate.as_view(), name='user-create'),  # Create a new user
    path('users/<int:pk>/', UserDetailUpdateDelete.as_view(), name='user-detail-update-delete'),  # Retrieve, update, or delete a user
    path('reviews/<int:pk>/like/', like_review, name='like-review'),  # Like or unlike a review
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),  # View user profile
    path('reviews/<int:pk>/comments/', CommentCreateView.as_view(), name='create-comment'),  # Add a comment to a review
    path('recommendations/', MovieRecommendationView.as_view(), name='movie-recommendations'),  # Get movie recommendations
]

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review, Profile, Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Use create_user to handle hashing
        return user

class ProfileSerializer(serializers.ModelSerializer):
    get_user_reviews = serializers.SerializerMethodField()  # Define method to get user reviews

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'get_user_reviews']  # Add user reviews to the profile

    def get_user_reviews(self, obj):
        return ReviewSerializer(obj.user.review_set.all(), many=True).data  # Fetch and serialize related reviews

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_date']

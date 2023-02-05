from django.contrib.auth.models import User
from rest_framework import serializers
from socialnetwork.models import UserProfile, UserPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    friends = UserSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'avatar', 'friends', 'created_at', 'profile_visibility', 'status', 'friends')

    def create(self, validated_data):
        # create user
        user = User.objects.create(
            username=validated_data['user']['username'],
            first_name=validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name'],
            email=validated_data['user']['email'],
        )

        # create profile
        profile = UserProfile.objects.create(user=user, avatar=validated_data['avatar'],
                                             status="Hey there! This is my default status!")

        return profile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ('text', 'image', 'created_at')

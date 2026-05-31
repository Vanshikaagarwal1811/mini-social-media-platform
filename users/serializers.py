from rest_framework import serializers
from .models import User, Post

from .models import User, Post, Comment
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']

class PostSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField()

    following_count = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [

            'id',

            'username',

            'email',

            'profile_picture',

            'followers_count',

            'following_count',
        ]

    def get_followers_count(self, obj):

        return obj.followers.count()

    def get_following_count(self, obj):

        return obj.following.count()
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

from .models import User, Post, Comment

from .serializers import (
    RegisterSerializer,
    PostSerializer,
    CommentSerializer,
    UserSerializer
)


@api_view(['GET', 'POST'])
def register_user(request):

    if request.method == 'GET':

        return Response({
            "message": "Send POST request to register user"
        })

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({

            'refresh': str(refresh),

            'access': str(refresh.access_token),
        })

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([])

def profile(request, username):

    try:

        user = User.objects.get(
            username=username
        )

    except User.DoesNotExist:

        return Response({

            'error': 'User not found'
        })

    posts = Post.objects.filter(
        user=user
    )

    user_serializer = UserSerializer(user)

    post_serializer = PostSerializer(
        posts,
        many=True
    )

    return Response({

        'user': user_serializer.data,

        'posts': post_serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def create_post(request):

    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(user=request.user)

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])

def get_posts(request):

    posts = Post.objects.all().order_by('-created_at')

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def like_post(request, post_id):
    print("USER:", request.user)
    print("AUTH:", request.auth)

    try:

        post = Post.objects.get(id=post_id)

    except Post.DoesNotExist:

        return Response({

            'error': 'Post not found'
        }, status=404)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

        return Response({

            'message': 'Post unliked'
        })

    else:

        post.likes.add(request.user)

        return Response({

            'message': 'Post liked'
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_post(request, post_id):

    try:

        post = Post.objects.get(id=post_id)

    except Post.DoesNotExist:

        return Response({

            'error': 'Post not found'
        }, status=404)

    if post.user != request.user:

        return Response({

            'error': 'You are not allowed to delete this post'
        }, status=403)

    post.delete()

    return Response({

        'message': 'Post deleted successfully'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_comment(request, post_id):

    try:

        post = Post.objects.get(id=post_id)

    except Post.DoesNotExist:

        return Response({

            'error': 'Post not found'
        }, status=404)

    text = request.data.get('text')

    if not text:

        return Response({

            'error': 'Comment text required'
        }, status=400)

    comment = Comment.objects.create(

        user=request.user,

        post=post,

        text=text
    )

    serializer = CommentSerializer(comment)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def follow_user(request, user_id):

    try:

        user_to_follow = User.objects.get(id=user_id)

    except User.DoesNotExist:

        return Response({

            'error': 'User not found'
        }, status=404)

    if request.user == user_to_follow:

        return Response({

            'error': 'You cannot follow yourself'
        }, status=400)

    if request.user in user_to_follow.followers.all():

        user_to_follow.followers.remove(request.user)

        return Response({

            'message': 'User unfollowed'
        })

    else:

        user_to_follow.followers.add(request.user)

        return Response({

            'message': 'User followed'
        })


def home(request):

    return render(request, 'index.html')
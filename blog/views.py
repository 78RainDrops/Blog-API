from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializers, CommentSerializers
from accounts.utils import verify_user

# Create your views here.


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
def post_list(request):
    # Get the token from the header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Authorization header is missing or invalid"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]
    user = verify_user(token)

    if not user:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # handle get
    if request.method == "GET":
        post = Post.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 1

        result_page = paginator.paginate_queryset(post, request)
        serializer = PostSerializers(result_page, many=True)
        return Response(serializer.data)

    # handle post
    elif request.method == "POST":
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_details(request, pk):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Authorization header is missing or invalid"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]
    user = verify_user(token)

    if not user:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializers(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        if post.author != user:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostSerializers(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if post.author != user:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def post_search(request):
    query = request.GET.get("q", "")
    post = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    serializer = PostSerializers(post, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def comment_list(request, post_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Authorization header is missing"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]
    user = verify_user(token)
    if not user:
        return Response(
            {"error", "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if request.method == "GET":
        comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 1

        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializers(result_page, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CommentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def comment_details(request, pk, post_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Authorization header is missing or invalid"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]
    user = verify_user(token)
    if not user:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        comment = Comment.objects.get(pk=pk, post_id=post_id)
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = CommentSerializers(comment)
        return Response(serializer.data)

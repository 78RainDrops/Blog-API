from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializers
from accounts.utils import verify_user

# Create your views here.


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
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
        serializer = PostSerializers(post, many=True)
        return Response(serializer.data)

    # handle post
    elif request.method == "POST":
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import django
from django.contrib.auth import get_user_model
from users.models import Post
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError
from users.serializers import PostSerializer
from django.db import transaction
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff')


class UserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PostApiView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        data = request.data['file'].read()
        try:
            records = json.loads(data)
        except Exception:
            return Response({"data": "invalid file"}, status=422)
        # user serializer and create post
        try:
            with transaction.atomic():
                for record in records:
                    serializer = PostSerializer(data=record)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response({"data": "records saved"})
        except django.db.utils.IntegrityError as e:
            return Response({"data": f"Invalid records: {e.__cause__}"}, status=500)

    def get(self, request, format=None):
        """
        Return a list of all posts.
        """
        current_user = request.user
        if current_user.is_staff:
            posts = Post.objects.all()
        else:
            posts = Post.objects.all().filter(user_id=current_user.id)

        serializer = PostSerializer([post for post in posts], many=True)
        return Response({"data": serializer.data})

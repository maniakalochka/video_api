from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import QuerySet
from videos.models import Video, Like
from django.shortcuts import get_object_or_404

from .serializers import LikeSerializer, VideoSerializer, UserLikesSerializer


class VideoDetailView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> QuerySet[Video]:  # type: ignore
        user = self.request.user

        if user.is_authenticated and user.is_staff:  # type: ignore
            return Video.objects.filter(owner=user)
        elif user.is_authenticated:
            return Video.objects.filter(is_published=True) | Video.objects.filter(owner=user)
        return Video.objects.filter(is_published=True)


class VideoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = VideoPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):  # type: ignore
            user = self.request.user

            if user.is_authenticated and user.is_staff:  # type: ignore
                return Video.objects.filter(owner=user)
            elif user.is_authenticated:
                return Video.objects.filter(is_published=True) | Video.objects.filter(owner=user)
            return Video.objects.filter(is_published=True)


class VideoLikesView(APIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        video = get_object_or_404(Video, id=id)
        like, created = Like.objects.get_or_create(video=video, user=request.user)
        if created:
            video.total_likes += 1
            video.save()
            return Response({"status": "liked"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        video = get_object_or_404(Video, id=id)
        like = Like.objects.filter(video=video, user=request.user).first()
        if like:
            like.delete()
            video.total_likes = max(0, video.total_likes - 1)
            video.save()
            return Response({"status": "unliked"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not liked"}, status=status.HTTP_400_BAD_REQUEST)

class PublishedVideoIDsView(APIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        elif not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        ids = list(Video.objects.filter(is_published=True).values_list(
            'id',
            'owner__username',
            'created_at',
            'name',
            'total_likes'))
        return Response({"ids": ids})


class TopUsersAPIView(generics.ListAPIView):
    serializer_class = UserLikesSerializer
    permission_classes = [permissions.AllowAny]

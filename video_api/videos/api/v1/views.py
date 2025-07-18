from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from videos.models import Video

from .serializers import VideoSerializer


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

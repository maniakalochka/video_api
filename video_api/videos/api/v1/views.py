from rest_framework import generics
from videos.models import Video

from .serializers import VideoSerializer


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

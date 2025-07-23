from django.contrib.auth import get_user_model
from rest_framework import serializers

from videos.models import Like, Video, VideoFile


User = get_user_model()

class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ["id", "file", "quality"]


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user"]


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "owner",
            "name",
            "is_published",
            "total_likes",
            "created_at",
            "files",
            "likes",
        ]

    def create(self, validated_data):
        return Video.objects.create(
            owner=self.context["request"].user,
            **validated_data,
        )


class UserLikesSerializer(serializers.ModelSerializer):
    likes_sum = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["username", "likes_sum"]

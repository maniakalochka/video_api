from django.contrib.auth import get_user_model
from django.utils import timezone
from videos.models import Video, VideoFile
import random

User = get_user_model()

def generate_test_videos(user_count=10_000, video_count=100_000):
    users = list(User.objects.order_by("id")[:user_count])

    videos = [
        Video(
            owner=random.choice(users),
            name=f"Video {i}",
            is_published=random.choice([True, False]),
            total_likes=random.randint(0, 1000),
            created_at=timezone.now(),
        )
        for i in range(video_count)
    ]
    Video.objects.bulk_create(videos, batch_size=1000)

    created_videos = list(Video.objects.order_by("-id")[:video_count])

    video_files = []
    for video in created_videos:
        for quality in VideoFile.Quality.values:
            video_files.append(VideoFile(video=video, quality=quality))
    VideoFile.objects.bulk_create(video_files, batch_size=1000)

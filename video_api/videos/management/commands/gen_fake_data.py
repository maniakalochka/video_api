import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ...models import Video, VideoFile, Like

User = get_user_model()

def generate_test_data(user_count=10_000, video_count=100_000, max_likes_per_video=50):
    print(f"Создание {user_count} пользователей...")

    hashed_pw = make_password("pass1234")

    users = []
    for i in range(user_count):
        user = User(
            username=f"user_{i}",
            email=f"user_{i}@example.com",
            is_staff=random.choice([True, False]),
            password=hashed_pw
        )
        users.append(user)

        if (i + 1) % 1000 == 0 or i + 1 == user_count:
            print(f" -> Подготовлено пользователей: {i + 1} / {user_count}", flush=True)

    User.objects.bulk_create(users, batch_size=1000)
    print("Пользователи созданы.")

    users = list(User.objects.order_by("-id")[:user_count])

    print(f"Создание {video_count} видео...", flush=True)

    videos = [
        Video(
            owner=random.choice(users),
            name=f"Video {i}",
            is_published=random.choice([True, False]),
            created_at=timezone.now(),
        )
        for i in range(video_count)
    ]
    Video.objects.bulk_create(videos, batch_size=1000)

    created_videos = list(Video.objects.order_by("-id")[:video_count])

    print("Создание файлов для видео...")

    video_files = []
    for video in created_videos:
        for quality in VideoFile.Quality.values:
            video_files.append(VideoFile(video=video, quality=quality))

    VideoFile.objects.bulk_create(video_files, batch_size=1000)

    print("Создание лайков...")

    likes = []
    video_likes_map = {}

    for video in created_videos:
        like_count = random.randint(0, max_likes_per_video)
        liked_users = random.sample(users, min(like_count, len(users)))

        for user in liked_users:
            likes.append(Like(video=video, user=user))

        video_likes_map[video.id] = len(liked_users)  # type: ignore

    Like.objects.bulk_create(likes, batch_size=1000)

    print("Обновление количества лайков у видео...")

    for video in created_videos:
        video.total_likes = video_likes_map.get(video.id, 0)  # type: ignore

    Video.objects.bulk_update(created_videos, ["total_likes"], batch_size=1000)

    print("Все данные сгенерированы.")

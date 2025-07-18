from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from videos.models import Video

User = get_user_model()


class VideoDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")  # type: ignore
        self.video = Video.objects.create(
            owner=self.user,
            name="Test Video",
            is_published=True,
        )
        self.detail_url = reverse("video-detail", kwargs={"pk": self.video.pk})

    def test_get_video_detail_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Video")  # type: ignore

    def test_get_video_detail_not_found(self):
        url = reverse("video-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class VideoListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")  # type: ignore
        self.video1 = Video.objects.create(
            owner=self.user,
            name="Test Video 1",
            is_published=True,
        )
        self.video2 = Video.objects.create(
            owner=self.user,
            name="Test Video 2",
            is_published=True,
        )
        self.list_url = reverse("video-list")

    def test_get_video_list_success(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # type: ignore
        self.assertEqual(response.data["results"][1]["name"], "Test Video 1")  # type: ignore
        self.assertEqual(response.data["results"][0]["name"], "Test Video 2")  # type: ignore

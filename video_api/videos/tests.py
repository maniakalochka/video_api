# tests/test_views.py
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from videos.models import Video

User = get_user_model()

class VideoDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')  # type: ignore
        self.video = Video.objects.create(
            owner=self.user,
            name="Test Video",
            is_published=True,
        )
        self.detail_url = reverse('video-detail', kwargs={'pk': self.video.pk})

    def test_get_video_detail_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Video')  # type: ignore

    def test_get_video_detail_not_found(self):
        url = reverse('video-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

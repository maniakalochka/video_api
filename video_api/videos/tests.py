from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from videos.models import Video

User = get_user_model()


class VideoDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            password="pass1234"
        )
        self.video = Video.objects.create(
            owner=self.user,
            name="Test Video",
            is_published=True,
            total_likes=0,
        )
        self.detail_url = reverse("video-detail", kwargs={"pk": self.video.pk})

    def test_get_video_detail_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test Video")  # type: ignore
        self.assertEqual(response.data["total_likes"], 0)  # type: ignore


    def test_get_video_detail_not_found(self):
        url = reverse("video-detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_video_detail_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)


class VideoListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            password="pass1234",
            is_staff=True
        )
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


class VideoDetailLikesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            password="pass1234",
            email="valid@mail.ru"
        )
        self.video = Video.objects.create(
            owner=self.user,
            name="Test Video",
            is_published=True,
            total_likes=0,
        )
        self.likes_url = reverse("video-likes", kwargs={"id": self.video.id})  # type: ignore

    def test_cannot_like_video_because_not_authenticated(self):
        self.likes_url = reverse("video-likes", kwargs={"id": self.video.id})  # type: ignore
        response = self.client.post(self.likes_url)
        print(response)
        self.assertEqual(response.status_code, 401)


    def test_like_video_success(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'pass1234'
        })
        token = response.data['access']  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) # type: ignore
        response = self.client.post(self.likes_url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "liked")  # type: ignore
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 1)  # type: ignore


class TestListIDs(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(  # type: ignore
            username="testuser",
            password="pass1234",
            is_staff=True
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username="testuser2",
            password="pass1234",
            is_staff=False
        )
        self.user3 = User.objects.create_user(  # type: ignore
            username="testuser3",
            password="pass1234",
            is_staff=False
        )
        self.video = Video.objects.create(
            owner=self.user2,
            name="Test Video",
            is_published=False,
            total_likes=0,
        )
        self.detail_url = reverse("video-ids")


    def test_get_video_ids_success_only_for_staff_users(self):
        client = APIClient()
        response = client.post('/login/', {'username': 'testuser', 'password': 'pass1234'})
        token = response.data['access']  # type: ignore
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)  # type: ignore

        client = APIClient()
        response = client.post('/login/', {'username': 'testuser3', 'password': 'pass1234'})
        token = response.data['access']  # type: ignore
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)  # type: ignore

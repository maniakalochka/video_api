from django.db.models import OuterRef, Subquery, Sum
from django.contrib.auth import get_user_model
from ..models import Video

User = get_user_model()


def get_video_statistics_by_subquery():
    likes_subquery = (
        Video.objects.filter(is_published=True, owner_id=OuterRef("pk"))
        .values("owner_id")
        .annotate(likes_sum=Sum("total_likes"))
        .values("likes_sum")
    )

    return User.objects.annotate(likes_sum=Subquery(likes_subquery)).order_by(
        "-likes_sum"
    )


def get_video_statistics_by_group_by():
    return (
        Video.objects.filter(is_published=True)
        .values("owner__username")
        .annotate(likes_sum=Sum("total_likes"))
        .order_by("-likes_sum")
    )

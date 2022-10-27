from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from common.models import CommonModel


class Club(CommonModel):

    """Club Model Definition"""

    class ClubEventChoices(models.TextChoices):
        TRACK_AND_FIELD = ("track_and_field", "육상")
        BALL_GAME = ("ball_game", "구기")
        RACKET_SPORTS = ("racket_sports", "라켓 스포츠")
        AQUATIC_SPORTS = ("auatic_sports", "수상 스포츠")
        GYMNASTICS = ("gymnastics", "체조")
        ICE_SPORTS = ("ice_sports", "빙상")
        SNOW_SPORTS = ("snow_sports", "설상")
        DANCE = ("dance", "무용")
        GYM_SPORTS = ("gym_sports", "Gym Sports")

    name = models.CharField(
        max_length=180,
        default="",
    )

    city = models.CharField(
        max_length=80,
        default="서울",
    )

    gu = models.CharField(
        max_length=80,
    )

    price = models.PositiveIntegerField()
    locker_room = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField(
        max_length=300,
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=250,
    )
    kind = models.CharField(
        max_length=20,
        choices=ClubEventChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="clubs",
    )
    amenities = models.ManyToManyField("clubs.Amenity", related_name="clubs",)

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clubs",
    )

    open_time = models.CharField(null=True, default="", max_length=20,)
    close_time = models.CharField(null=True, default="", max_length=20,)

    def __str__(self):
        return self.name

    def total_amenities(club):
        return club.amenities.count()

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):

    """Amenity Definiton"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        EXPERIENCE = ("experience", "Experience")

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="booking",
    )
    club = models.ForeignKey(
        "clubs.Club",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="booking",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="booking",
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"

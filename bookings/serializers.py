from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests"
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if Booking.objects.filter(experience_time=data["experience_time"]).exists():
            raise serializers.ValidationError(
                "This time are already taken."
            )
        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_time",
            "guests",
        )

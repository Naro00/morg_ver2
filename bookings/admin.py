from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "club",
        "experience",
        "experience_time",
        "guests",
    )
    list_filter = ("kind",)

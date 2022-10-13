from django.urls import path
from . import views


urlpatterns = [
    path("", views.Clubs.as_view()),
    path("<int:pk>", views.ClubDetail.as_view()),
    path("<int:pk>/reviews", views.ClubReviews.as_view()),
    path("<int:pk>/photos", views.ClubPhotos.as_view()),
    path("<int:pk>/amenities", views.ClubAmenities.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>/", views.AmenityDetail.as_view()),
]

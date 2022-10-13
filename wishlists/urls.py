from django.urls import path
from .views import WishlistToggle, Wishlists, WishlistDetail

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/clubs/<int:club_pk>", WishlistToggle.as_view()),
]

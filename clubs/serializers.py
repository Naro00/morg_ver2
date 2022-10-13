from rest_framework import serializers
from .models import Amenity, Club
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description",)


class ClubDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True,)
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = "__all__"

    def get_rating(self, club):
        return club.rating()

    def get_is_owner(self, club):
        request = self.context["request"]
        return club.owner == request.user

    def get_is_liked(self, club):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, clubs__pk=club.pk,).exists()


class ClubListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = (
            "pk",
            "name",
            "city",
            "gu",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, club):
        request = self.context["request"]
        return club.owner == request.user

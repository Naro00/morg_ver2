from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Perk, Experience
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perk = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photo = PhotoSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, experiences__pk=experience.pk,).exists()


class ExperienceListSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "city",
            "gu",
            "price",
            "rating",
            "is_host",
            "photo",
        )

    def get_rating(self, experience):
        return experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

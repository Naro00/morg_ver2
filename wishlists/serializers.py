from rest_framework.serializers import ModelSerializer
from clubs.serializers import ClubListSerializer
from .models import Wishlist


class WishlistsSerializer(ModelSerializer):

    clubs = ClubListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "clubs",
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from clubs.models import Club
from .models import Wishlist
from .serializers import WishlistsSerializer


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistsSerializer(
            all_wishlists, many=True, context={"request": request},)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistsSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistsSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist, context={"request": request},)
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistsSerializer(
                wishlist,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_club(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise NotFound

    def put(self, request, pk, club_pk):
        wishlist = self.get_list(pk, request.user)
        club = self.get_club(club_pk)
        if wishlist.clubs.filter(pk=club.pk).exists():
            wishlist.clubs.remove(club)
        else:
            wishlist.clubs.add(club)
        return Response(status=HTTP_200_OK)

from django.conf import settings
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound, NotAuthenticated, ParseError, PermissionDenied,)
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Club
from categories.models import Category
from .serializers import AmenitySerializer, ClubListSerializer, ClubDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True,)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity, data=request.data, partial=True,)
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitySerializer(update_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ClubAmenities(APIView):
    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        club = self.get_object(pk)
        serializer = AmenitySerializer(
            club.amenities.all()[start:end], many=True,)
        return Response(serializer.data)


class Clubs(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_clubs = Club.objects.all()
        serializer = ClubListSerializer(
            all_clubs, many=True, context={"request": request},)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClubDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError(
                        "The category kind should be 'Clubs'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    club = serializer.save(
                        owner=request.user, category=category,)
                    amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    club.amenities.add(amenity)
                serializer = ClubDetailSerializer(club)
                return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors)


class ClubDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        club = self.get_object(pk)
        serializer = ClubDetailSerializer(club, context={"request": request},)
        return Response(serializer.data)

    def put(self, request, pk):
        club = self.get_object(pk)
        if club.owner != request.user:
            raise PermissionDenied
        elif request.user.is_authenticated:
            serializer = ClubDetailSerializer(
                club, data=request.data, partial=True,)
            if serializer.is_valid():
                update_club = serializer.save()
                return Response(ClubDetailSerializer(update_club).data)
            else:
                return Response(serializer.errors)

    def delete(self, request, pk):
        club = self.get_object(pk)
        if club.owner != request.user:
            raise PermissionDenied
        club.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ClubReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        club = self.get_object(pk)
        serializer = ReviewSerializer(
            club.reviews.all()[start:end], many=True,)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user, club=self.get_object(pk),)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class ClubPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        club = self.get_object(pk)
        if request.user != club.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(club=club)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

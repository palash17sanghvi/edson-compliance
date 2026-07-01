from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bookings
from .serializers import BookingSerializer


@api_view(['GET'])
def get_bookings(request):

    bookings = Bookings.objects.all()

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)

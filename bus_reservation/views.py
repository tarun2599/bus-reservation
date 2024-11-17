from datetime import datetime
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Bus, Reservation
from .serializers import BusSerializer, ReservationSerializer, SearchBusSerializer

@swagger_auto_schema(
    method='get',
    query_serializer=SearchBusSerializer,
    responses={
        200: BusSerializer(many=True),
        400: 'Bad Request'
    },
    operation_description="Search for buses based on source, destination, and date",
    operation_summary="Search Buses"
)
@api_view(['GET'])
def search_buses(request):
    """Search for buses based on source, destination, and date."""
    serializer = SearchBusSerializer(data=request.query_params)
    if serializer.is_valid():
        source = serializer.validated_data['source']
        destination = serializer.validated_data['destination']
        date = serializer.validated_data['date']
        day_of_week = date.strftime('%A')

        # Get all buses for the route first
        buses = Bus.objects.filter(source=source, destination=destination)
        
        # Then filter for frequency manually
        filtered_buses = [
            bus for bus in buses
            if day_of_week in bus.frequency
        ]
        
        bus_serializer = BusSerializer(filtered_buses, many=True)
        return Response(bus_serializer.data)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['bus_id', 'user_name', 'date', 'seats_reserved'],
        properties={
            'bus_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'user_name': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'seats_reserved': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ),
    responses={
        200: ReservationSerializer,
        400: 'Bad Request - Not enough seats available',
        404: 'Bus not found'
    },
    operation_description="Reserve seats on a specific bus",
    operation_summary="Reserve Seats"
)
@api_view(['POST'])
def reserve_seats(request):
    """Reserve seats on a specific bus."""
    data = request.data
    try:
        bus = Bus.objects.get(id=data['bus_id'])
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()

        # Check seat availability
        total_reserved = Reservation.objects.filter(bus=bus, date=date).aggregate(
            models.Sum('seats_reserved'))['seats_reserved__sum'] or 0
        available_seats = bus.capacity - total_reserved

        if data['seats_reserved'] > available_seats:
            return Response({"error": "Not enough seats available"}, status=400)

        # Create reservation
        reservation = Reservation.objects.create(
            user_name=data['user_name'],
            bus=bus,
            date=date,
            seats_reserved=data['seats_reserved']
        )
        return Response(ReservationSerializer(reservation).data)
    except Bus.DoesNotExist:
        return Response({"error": "Bus not found"}, status=404)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'user_name',
            openapi.IN_QUERY,
            description="Name of the user",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: ReservationSerializer(many=True),
        400: 'Bad Request - User name is required'
    },
    operation_description="View all reservations for a specific user",
    operation_summary="View Reservations"
)
@api_view(['GET'])
def view_reservations(request):
    """View all reservations for a specific user."""
    user_name = request.query_params.get('user_name')
    if not user_name:
        return Response({"error": "User name is required"}, status=400)

    reservations = Reservation.objects.filter(user_name=user_name)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import room_serializer



@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = room_serializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, id):
    room = Room.objects.get(id=id)
    serializer = room_serializer(room)
    return Response(serializer.data)
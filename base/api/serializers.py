from rest_framework.serializers import ModelSerializer
from base.models import Room


class room_serializer(ModelSerializer):
    class Meta():
        model = Room
        fields = '__all__'
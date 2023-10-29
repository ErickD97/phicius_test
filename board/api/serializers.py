from rest_framework import serializers


class NewMoveStructureSerializer(serializers.Serializer):
    position = serializers.CharField()
    board_id = serializers.IntegerField()

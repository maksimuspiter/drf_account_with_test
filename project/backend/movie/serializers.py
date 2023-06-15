from rest_framework import serializers
from .models import Movie, Resource


def is_rating(value):
    if value < 1:
        raise serializers.ValidationError("Value cannot be lower than 1.")
    elif value > 10:
        raise serializers.ValidationError("Value cannot be higher than 10")


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[is_rating])

    class Meta:
        model = Movie
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["likes"] = instance.liked_by.count()

    #     return representation

    def to_internal_value(self, data):
        resource_data = data["resource"]

        return super().to_internal_value(resource_data)

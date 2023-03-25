from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


def create(self, validated_data):
    instance = self.Meta.model(**validated_data)
    instance.set_password(validated_data["password"])
    instance.save()
    return instance



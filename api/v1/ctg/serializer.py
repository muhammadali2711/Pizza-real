from rest_framework import serializers

from Site.models import Category



class CtgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

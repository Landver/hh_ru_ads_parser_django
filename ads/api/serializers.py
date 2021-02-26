from rest_framework import serializers

from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    # Сериализация модели объявлений
    class Meta:
        model = Ad
        fields = '__all__'

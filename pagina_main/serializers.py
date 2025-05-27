from rest_framework import serializers
from django.db.models import Avg
from .models import Anime, UserAnime

class UserAnimeSerializer(serializers.ModelSerializer):
    anime = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Anime.objects.all()
    )

    class Meta:
        model = UserAnime
        fields = ['id', 'anime', 'status', 'score']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance, created = UserAnime.objects.update_or_create(
            user=validated_data['user'],
            anime=validated_data['anime'],
            defaults={
                'status': validated_data.get('status', 'plan_to_watch'),
                'score': validated_data.get('score', None),
            }
        )
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # No permitir cambiar el usuario
        return super().update(instance, validated_data)


class AnimeSerializer(serializers.ModelSerializer):
    avg_score = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = ['id', 'title', 'slug', 'image', 'format', 'status', 'avg_score']

    def get_avg_score(self, obj):
        avg = obj.user_animes.filter(score__isnull=False).aggregate(average=Avg('score'))['average']
        return round(avg, 2) if avg is not None else None

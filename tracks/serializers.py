from rest_framework import serializers
from tracks.models import Track
from tracks.providers import GenericProvider

class TrackSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  uploaded = serializers.BooleanField(read_only=True)
  created_at = serializers.DateTimeField(read_only=True)

  # ===============
  # Writable fields
  # ===============
  # use the choices in the Track model

  provider = serializers.ChoiceField(choices=Track.CHOICES)
  file = serializers.FileField(write_only=True, allow_empty_file=False)
  title = serializers.CharField(write_only=True)
  description = serializers.CharField(write_only=True)

  # ===============
  # Provider fields
  # ===============

  provider_id = serializers.CharField(read_only=True)
  provider_url = serializers.URLField(read_only=True)
  provider_artwork_url = serializers.URLField(read_only=True)
  provider_title = serializers.CharField(read_only=True)
  provider_description = serializers.CharField(read_only=True)
  provider_permalink = serializers.URLField(read_only=True)
  provider_created_at = serializers.CharField(read_only=True)

  def create(self, validated_data):
    track = Track.objects.create(
      provider = validated_data.get('provider')
    )
    return GenericProvider(track).upload(
      file=validated_data.get('file'),
      title=validated_data.get('title'),
      description=validated_data.get('description')
    )
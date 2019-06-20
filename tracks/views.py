from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from tracks.models import Track
from tracks.providers import GenericProvider
from tracks.serializers import TrackSerializer

class TrackViewSet(viewsets.ViewSet):
  queryset = Track.objects.all()
  serializer_class = TrackSerializer

  def list(self, request):
    queryset = list(Track.objects.all())
    data = []
    for track in queryset:
      retrieved = GenericProvider(track).retrieve()
      data.append(retrieved)
    serializer = TrackSerializer(data, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    serializer = TrackSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
  
  def retrieve(self, request, pk=None):
    track = get_object_or_404(Track, id=pk)
    retrieved = GenericProvider(track).retrieve
    serializer = TrackSerializer(retrieved)
    return Response(serializer.data)
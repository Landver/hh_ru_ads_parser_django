from rest_framework import generics

from .api.serializers import AdSerializer

from .models import Ad

import logging

logger = logging.getLogger('ads')

class AdListView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        logger.info(f'Got the page with id: {request.data["id"]}')
        return self.retrieve(request, *args, **kwargs)

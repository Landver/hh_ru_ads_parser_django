from rest_framework import generics

from .api.serializers import AdSerializer

from .models import Ad

import logging

logger = logging.getLogger('ads')


class AdListView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def post(self, request, *args, **kwargs):
        logger.info('posted')
        return self.create(request, *args, **kwargs)


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'

    def get(self, request, id, *args, **kwargs):
        logger.info(f'Got the page with id: {str(id)}')
        return self.retrieve(request, *args, **kwargs)

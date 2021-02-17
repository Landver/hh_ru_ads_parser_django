from rest_framework import generics

from .api.serializers import AdSerializer

from rest_framework.exceptions import ValidationError

from .models import Ad

import logging

logger = logging.getLogger('ads')


class AdListView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def post(self, request, *args, **kwargs):
        try:
            logger.info('Posted an ad with url: {}'.format(request.POST['vacancy_url']))
            return self.create(request, *args, **kwargs)
        except ValidationError:
            logger.warning("{} doesn't posts".format(request.POST['vacancy_url']))


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'

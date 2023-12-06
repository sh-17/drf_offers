import logging

from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Offer
from .serializers import OfferSerializer
from rest_framework import viewsets
from .mypaginations import MyLimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .utils import success_true_response, success_false_response
from rest_framework.filters import OrderingFilter

logger = logging.getLogger("api.views")


class OfferModelViewSet(viewsets.ModelViewSet, GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    # Filter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    # Searching
    filter_backends = [SearchFilter]
    search_fields = ['^title']

    # ordering
    filter_backends = [OrderingFilter]
    ordering_fields = ['status']

    # Ordering
    # from rest_framework.filters import OrderingFilter

    # filter_backends = [OrderingFilter]

    # Pagination -- created pagination.py file and create class & set here
    pagination_class = MyLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # Perform additional filtering based on query parameters
            # For example, you can filter based on a request parameter named 'active'
            active_filter = request.query_params.get('active')

            if active_filter:
                queryset = queryset.filter(active=active_filter)

            #ordering
            queryset = self.filter_queryset(queryset)

            # pagination
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info('Data listed successfully')
                return self.get_paginated_response(
                    success_true_response(message='Data retrieved successfully', data=serializer.data))

            serializer = self.get_serializer(queryset, many=True)
            logger.info('Data listed successfully')
            return Response(success_true_response(message='Data retrieved successfully', data=serializer.data))
        except Exception as e:
            logger.error(f"An error occurred during listing: {e}")
            return Response(success_false_response(message='Failed to retrieve data', data={'error': str(e)}))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info('Offer created successfully')  # Log info message
            return Response(
                success_true_response(message='Offer created successfully', data={"Success": serializer.data},))
        except Exception as e:
            logger.error(f"An error occurred while creating data: {e}")  # Log error message
            return Response(success_false_response(message='Failed to create Offer', data={'error': str(e)}),
                            status=400)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info('Offer updated successfully')  # Log info message
            return Response(success_true_response(message='Offer updated successfully'))
        except Exception as e:
            logger.error(f"An error occurred while updating data: {e}")  # Log error message
            return Response(success_false_response(message='Failed to update Offer', data={'error': str(e)}),
                            status=400)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_delete(instance)
            logger.info('Offer deleted successfully')  # Log info message
            return Response(success_true_response(message='Offer deleted successfully'))
        except Exception as e:
            logger.error(f"An error occurred while deleting data: {e}")  # Log error message
            return Response(success_false_response(message='Failed to delete Offer', data={'error': str(e)}),
                            status=400)



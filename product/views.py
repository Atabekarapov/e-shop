from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions as p, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .filters import ProductFilter
from .models import *
from .serializers import *

#
# class ProductsList(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductDetail(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class CreateProduct(CreateAPIView):
#     queryset = Product.objects.all()
#     permission_classes = [permissions.IsAdminUser]
#     serializer_class = CreateUpdateProductSerializer
#
#
# class UpdateProduct(UpdateAPIView):
#     queryset = Product.objects.all()
#     permission_classes = [permissions.IsAdminUser]
#     serializer_class = CreateUpdateProductSerializer
#
#
# class DeleteProduct(DestroyAPIView):
#     queryset = Product.objects.all()
#     permission_classes = [permissions.IsAdminUser]


class MyPagination(PageNumberPagination):
    page_size = 2


class CategoriesList(ListAPIView):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.all()
    pagination_class = MyPagination
    filter_backends  = [DjangoFilterBackend]
    # filterset_fields = ['title']
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return  ProductSerializer
        return  CreateUpdateProductSerializer

    def get_permissions(self):
        # if self.action == 'list' or self.action == 'retrieve':
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [p.IsAdminUser]
        return [permission() for permission in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:

            queryset =  queryset.filter(Q(title__icontains=q) |
                            Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



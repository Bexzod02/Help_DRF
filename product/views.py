import json

from django.db.models import Q, Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from rest_framework.response import Response
from product.models import Product
from rest_framework import generics, status, mixins, permissions, authentication

from .permissions import IsOwnerOrReadOnly
from .serializer import ProductSerializer
from .peginator import CustomPagination
from rest_framework.decorators import api_view


def api_home_(request):
    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except:
        print("except")
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    data["params"] = request.GET
    return JsonResponse(data)


def api_home_(request):
    product = Product.objects.all().order_by("?").first()
    data = {}
    if product:
        data['id'] = product.id
        data['title'] = product.title
        data['content'] = product.content
        data['price'] = product.price
    return JsonResponse(data)


@api_view(["GET"])
def api_home_(request):
    product = Product.objects.all().order_by("?").first()
    data = {}
    if product:
        data['id'] = product.id
        data['title'] = product.title
        data['price'] = product.price
    return Response(data)


@api_view(["GET"])
def api_home(request):
    product = Product.objects.all()
    data = {}
    if product:
        data = ProductSerializer(product, many=True).data
    return Response(data)


@api_view(['POST'])
def api_post(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET'])
def api_detail(request, pk):
    instance = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance)
    return Response(serializer.data, status=201)


@api_view(['PUT'])
def api_put(request, pk):
    instance = Product.objects.get(id=pk)
    serializer = ProductSerializer(data=request.data, instance=instance)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response({"detail": "Is not allowed"})


@api_view(['DELETE'])
def api_delete(request, pk):
    instance = Product.objects.get(id=pk)
    instance.delete()
    return Response(status=204)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rud(request, pk):
    instance = Product.objects.get(id=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=201)

    if request.method == 'PUT':
        serializer = ProductSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    # return Response({"detail": "Is not allowed"})

    if request.method == 'PATCH':
        serializer = ProductSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    # return Response({"detail": "Is not allowed"})

    if request.method == 'DELETE':
        instance.delete()
        return Response({'delete':'Successful deleted !'}, status=204)

### CBV


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Product.objects.none()
        return qs.filter(user = request.user)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content' or None)
        if content is None:
            content = title
        serializer.save(content=content)

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]


class ProductRetrive(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')
        c = self.request.query_params.get('c')

        q_condition = Q()
        if q:
            qs = Q(title__icontains=q)
        c_condition = Q()
        if c:
            qs = Q(description__icontanins=c)
        return qs.filter(q_condition, c_condition)


class ProductRetriveEditdeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Successfuly deleted item'}, status=status.HTTP_204_NO_CONTENT)

    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]


class DayliProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super(DayliProduct, self).get_queryset()

        return qs

    def filter_qs(self, date):
        return self.get_queryset().filter(created_at__contains=date)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        lst = qs.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id'))
        data = {
            "count": qs.count(),
            "results": []
        }
        for i in lst:
            data['results'].append({
                'date': i.get('date'),
                'count': i.get('count'),
                'products': [{'id': j.id, 'title': j.title} for j in self.filter_qs(i.get('date'))]
            })
        return Response(data)


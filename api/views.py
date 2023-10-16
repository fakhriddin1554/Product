from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from blog.models import Category,Post
from main.models import Product, Category as ProductCategory
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializers import CategorySerializer,TaskSerizalier
from .models import Category as TaskCategory, Task
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from main.serializers import ProductCategorySerializer, ProductSerializer
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from authentication.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from authentication.serializers import RegisterSerializer,LoginSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters



class RegisterUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = serializer.get_token(user)
        return Response(data={"key": token.key})



class LoginUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(email=serializer.validated_data.get("email")).first()
        token = serializer.get_token(user=user)
        return Response(data={"key":token.key})



class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(queryset, many=True)
        return Response(data=serializer.data)
    
    def create(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(ProductCategory, pk=pk)
        serializer = ProductCategorySerializer(instance=instance)
        return Response(data=serializer.data)
    
    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass



class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()




class UpdateDestroyAPIView(mixins.UpdateModelMixin,mixins.DestroyModelMixin, GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CategoryListCreateGenericAPIView(GenericAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class CategoryRetrieveUpdateDestroyGenericAPIView(GenericAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    lookup_url_kwarg = 'slug'

    def get(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        self.get_object().delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter,rest_filters.OrderingFilter)
    filterset_fields = ('title', 'price')
    search_fields = ['title', 'description']
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        return super().perform_create(serializer)



class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'



class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        cats = TaskCategory.objects.all()
        serializer = CategorySerializer(instance=cats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cat = TaskCategory.objects.create(**serializer.validated_data)
        cat_sr = CategorySerializer(cat)
        return Response(data=cat_sr.data, status=status.HTTP_201_CREATED)
    

class CategoryRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, slug):
        category = get_object_or_404(TaskCategory, slug=slug)
        serializer = CategorySerializer(instance=category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        category = get_object_or_404(TaskCategory, slug=slug)
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=category, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        category = get_object_or_404(TaskCategory, slug=slug)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=category, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        category = get_object_or_404(TaskCategory, slug=slug)
        category.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)



class TaskListCreateAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerizalier(instance=tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerizalier(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(**serializer.validated_data)
        task_sr = TaskSerizalier(task)
        return Response(data=task_sr.data, status=status.HTTP_201_CREATED)
    

class TaskRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerizalier(instance=task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerizalier(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=task, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerizalier(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=task, validated_data=serializer.validated_data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)




@api_view(http_method_names=["GET", "POST", "PUT"])
@permission_classes([IsAdminUser])
def main(request: Request):
    #print(request.data, type(request.data))
    #print(request.query_params)
    #print(request.user, request.auth)
    #print(request.META)
    content = {
        'user':str(request.user),
        'auth':str(request.auth),
    }
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data}, status=status.HTTP_201_CREATED)
    cats = list(Category.objects.all().values())
    cats.append({"auth":content})
    return Response(data=cats, status=status.HTTP_200_OK)


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        post = Post.objects.filter(pk=pk)
        data = list(post.values())
        return Response(data={"post":data})


class ProductCategoryListCreateAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    """ This view response us all product categories list """
    def get(self, request):
        cats = ProductCategory.objects.all()
        data = list(cats.values())
        return Response(data={"categories": data})
    
    def post(self, request):
        title = request.data.get("title")
        if title is None:
            raise ValidationError(detail={"title": "This field is required."})
        category = ProductCategory.objects.create(title=title, description=request.data.get("description"))
        data = {
            "title": category.title,
            "slug" : category.slug,
            "description": category.description
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    

class ProductCategoryRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        cat = ProductCategory.objects.filter(pk=pk)
        data = list(cat.values())
        return Response(data=data)

    def put(self, request, pk):
        cats = ProductCategory.objects.filter(pk=pk)
        if cats.first():
            cat = cats.first()
            title = request.data.get("title", cat.title)
            slug = request.data.get("slug", cat.slug)
            description = request.data.get("description", cat.description)
            cat.title = title
            cat.slug = slug
            cat.description = description
            cat.save()
            return Response(data=list(cats.values()))
        return Response(data={"error": f"{pk} doesn't exist!"})

    #def patch(self, request, pk):
       # pass

    def delete(self, request, pk):
        cats = ProductCategory.objects.filter(pk=pk)
        if cats.first():
            cat = cats.first()
            cat.delete()
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"error": f"{pk} doesn't exist!"})
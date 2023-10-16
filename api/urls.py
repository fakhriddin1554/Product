from django.urls import path
from .views import main,PostDetail,ProductCategoryListCreateAPIView,ProductCategoryRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView,CategoryRetrieveUpdateDestroyAPIView, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView, CategoryListCreateGenericAPIView,CategoryRetrieveUpdateDestroyGenericAPIView, ProductListCreateAPIView,ProductRetrieveUpdateDestroyAPIView,CategoryViewSet,ProductModelViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r'products', ProductModelViewSet, basename="product")


urlpatterns = [
    path('', main, name="main"),
    path('main/cats/', CategoryViewSet.as_view({"get":"list", "post": "create"}), name="main-cats"),
    path('main/cat/<int:pk>/', CategoryViewSet.as_view({"get":"retrieve", "put":"update","patch":"partial_update", "delete":"destroy" }), name="cat-retrieve"),
    path('main/cat/<slug:slug>/', CategoryRetrieveUpdateDestroyGenericAPIView.as_view(), name="main-cat-detail"),
    path('main/products/', ProductListCreateAPIView.as_view(), name="product-list-create"),
    path('main/product/<slug:slug>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-get-update-delete"),
    path('task/cats/', CategoryListCreateAPIView.as_view(),name="task-cats-list"),
    path('task/cat/<slug:slug>/', CategoryRetrieveUpdateDestroyAPIView.as_view(),name="task-cat-detail"),
    path('tasks/', TaskListCreateAPIView.as_view(), name="task-list"),
    path('task/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name="task-detail"),
    path('post/<int:pk>/', PostDetail.as_view(),name="post-detail"),
    path('cats/', ProductCategoryListCreateAPIView.as_view(), name="cats-list"),
    path('cat/<int:pk>/',ProductCategoryRetrieveUpdateDestroyAPIView.as_view(), name="cat-detail")
] + router.urls
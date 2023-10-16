from django.urls import path
from .views import post_list, PostDetail,PostCreate,PostUpdate,PostDelete,PostList

urlpatterns = [
    path('', PostList.as_view(), name="posts-list"),
    path('create/', PostCreate.as_view(), name="post-create"),
    path('update/<slug:slug>/', PostUpdate.as_view(), name="post-update"),
    path('delete/<slug:slug>/', PostDelete.as_view(), name="post-delete"),
    path('<slug:slug>/', PostDetail.as_view(), name="post-detail")
    
]
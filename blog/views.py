from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


#class PostList(View):
    #def get(self, request, *args, **kwargs):
        #posts = Post.objects.all()
        #return render(request, "post/list.html", {"posts": posts})

class PostList(ListView):
    queryset = Post.objects.filter(published = True).order_by("-id")
    template_name = "post/list.html"
    context_object_name = "posts"
    paginate_by = 4



def post_list(request):
    queryset = Post.objects.filter(published = True).order_by("-id")
    return render(request, "post/list.html", {"posts": queryset})


class PostDetail(DetailView):
    pk_url_kwarg = None
    queryset = Post.objects.all()
    template_name = "post/detail.html"
    context_object_name = "post"


#class PostCreate(View):
#    def get(self, request):
#        form = PostForm
#        return render(request, "post/create.html", {"form": form} )
#    
#    def post(self, request):
#        form = PostForm(data=request.POST, files=request.FILES)
#        if form.is_valid():
#            form.save()
#            return redirect("posts-list")
#        return render(request, "post/create.html", {"form": form} )
    
class PostCreate(LoginRequiredMixin,CreateView):
    login_url = '/auth/login/'
    redirect_field_name = 'index'
    model = Post
    form_class = PostForm
    template_name = "post/create.html"
    success_url = reverse_lazy("posts-list")


class PostUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/auth/login/'
    redirect_field_name = 'index'
    model = Post
    queryset = Post.objects.all()
    pk_url_kwarg = None
    form_class = PostForm
    template_name = "post/update.html"
    success_url = reverse_lazy("posts-list")


class PostDelete(LoginRequiredMixin,DeleteView):
    login_url = '/auth/login/'
    redirect_field_name = 'index'
    model = Post
    queryset = Post.objects.all()
    pk_url_kwarg = None
    template_name = "post/delete.html"
    success_url = reverse_lazy("posts-list")
    
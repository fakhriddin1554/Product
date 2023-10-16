from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        fields = ('title', 'slug', 'description', 'category', 'author', 'published', 'image', 'publish_date', "tag")
        model = Post
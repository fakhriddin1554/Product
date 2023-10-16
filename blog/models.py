from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        db_table = "categories"



class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tags"
    

class Post(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="posts/%Y/%m/%d")
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "posts"



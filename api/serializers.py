import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Category,Task

class PostModel:
    def __init__(self, title, content) -> None:
        self.title = title
        self.content = content

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=2000)

def encode():
    model = PostModel(title="Test title", content="Test content")
    model_sr = PostSerializer(instance=model)
    print(model_sr.data, type(model_sr.data), sep="\n")
    json = JSONRenderer().render(data=model_sr.data)
    print(json)

def decode():
    json = b'{"title":"Test title","content":"Test content"}'
    stream = io.BytesIO(json)
    data = JSONParser().parse(stream=stream)
    serializer = PostSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance
    

class TaskSerizalier(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
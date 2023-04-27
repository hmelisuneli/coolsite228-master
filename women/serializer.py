import io

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from women.models import Women


# class HeroModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class HeroSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
         model = Women
         fields = "__all__"


    # title = serializers.CharField(max_length=225)
    # content = serializers.CharField()
    # time_create = serializers.DateTimeField(read_only=True)
    # time_update = serializers.DateTimeField(read_only=True)
    # is_published = serializers.BooleanField(default=True)
    # cat_id = serializers.IntegerField()
    #
    # def create(self, validated_data):
    #     return Women.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data("title", instance.title)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.time_update = validated_data.get("time_update", instance.time_update)
    #     instance.is_published = validated_data.get("is_published", instance.is_published)
    #     instance.cat_id = validated_data.get("cat_id", instance.cat_id)
    #     instance.save()
    #     return instance
    #


# def encode():
#     model = HeroModel('Nosorog', 'Content: Nosorog')
#     model_sr = HeroSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def  decode():
#     stream = io.BytesIO(b'{"title":"Nososrog","content":"Content:Nosorog"}')
#     data = JSONRenderer().parse(stream)
#     serializers = HeroSerializer(data=data)
#     serializers.is_valid()
#     print(serializers.validated_data)


from rest_framework import serializers

from women.models import Women


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Women
        fields = ('title', 'cat_id')


from rest_framework import serializers
from ...models import Task
from django.contrib.auth.models import User

class TaskSerializer (serializers.ModelSerializer):
    absolute_url=serializers.SerializerMethodField(method_name="get_absolute_url")
    class Meta:
        model=Task
        fields = ['title', 'complete', 'id','absolute_url']
    def get_absolute_url(self,obj):
        request=self.context.get("request")
        return request.build_absolute_uri(obj.pk)
    



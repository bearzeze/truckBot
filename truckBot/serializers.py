from rest_framework import serializers
from .models import InformedHistory, PostHistory


class InformedHistorySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    count_drivers = serializers.IntegerField(source="drivers_informed_count")
    username = serializers.CharField(source="user.username")
    
    class Meta:
        model = InformedHistory
        fields = ['load_id', 'date', 'count_drivers', 'username']
    
    def get_date(self, obj):
        return obj.formatted_date()
    
    
class PostHistorySerializer(serializers.ModelSerializer):
    load_description = serializers.CharField()
    landstar_id = serializers.IntegerField()
    username = serializers.CharField(source='user.username', read_only=True)
    date = serializers.CharField(source='formatted_date', read_only=True)
    
    class Meta:
        model = PostHistory
        fields = ['load_description','landstar_id', 'date', 'username']

    

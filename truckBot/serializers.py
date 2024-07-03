from rest_framework import serializers
from .models import LoadHistory


class LoadHistorySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    count_drivers = serializers.IntegerField(source="drivers_informed_count")
    username = serializers.CharField(source="user.username")
    
    class Meta:
        model = LoadHistory
        fields = ['load_id', 'date', 'count_drivers', 'username']
    
    
    def get_date(self, obj):
        return obj.formatted_date()

from rest_framework import serializers
from .models import LogHistory


class LogHistorySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    count_drivers = serializers.IntegerField(source="drivers_informed_count")
    
    class Meta:
        model = LogHistory
        fields = ['load_id', 'date', 'count_drivers']
    
    
    def get_date(self, obj):
        return obj.formatted_date()

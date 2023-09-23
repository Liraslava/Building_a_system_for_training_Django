from rest_framework import serializers
from .models import Lesson, LessonView
from rest_framework import serializers

class ProductStatisticsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    total_lessons_viewed = serializers.IntegerField()
    total_time_spent_minutes = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_users_enrolled = serializers.IntegerField()
    percent_acquisition = serializers.DecimalField(max_digits=5, decimal_places=2)

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url']

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['user', 'lesson', 'watched', 'watched_percentage', 'timestamp']
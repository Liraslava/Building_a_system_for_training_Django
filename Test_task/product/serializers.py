from rest_framework import serializers
from .models import Lesson, LessonView

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url']

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['user', 'lesson', 'watched', 'watched_percentage', 'timestamp']
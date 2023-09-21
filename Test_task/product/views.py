from django.shortcuts import render
from rest_framework import generics
from .models import Lesson, LessonView
from .serializers import LessonSerializer, LessonViewSerializer, LessonSerializer
from .models import Lesson, Product, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        # We return only lessons to which the user has access
        return Lesson.objects.filter(product__in=user.products.all())

class LessonViewListView(generics.ListAPIView):
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user
        # Returning information about viewing lessons for the current user
        return LessonView.objects.filter(user=user)


def index_page(request):
    return render(request, 'index.html')


class LessonListViewStatus(APIView):
    def get(self, request, user_id, product_id):
        try:
            user_profile = User.objects.get(user_id=user_id)
            product = Product.objects.get(id=product_id)


            if product not in user_profile.products_access.all():
                return Response({'error': 'Пользователь не имеет доступ к данному продукту'}, status=status.HTTP_403_FORBIDDEN)

            lessons = Lesson.objects.filter(product=product)
            lesson_serializer = LessonSerializer(lessons, many=True)
            return Response(lesson_serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)
from django.shortcuts import render
from rest_framework import generics
from .models import Lesson, LessonView
from .serializers import LessonSerializer, LessonViewSerializer, LessonSerializer
from .models import Lesson, Product, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F
from django.db.models.functions import Coalesce
from django.db.models import FloatField
from decimal import Decimal

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

            # check if the user has access to the product
            if product not in user_profile.products_access.all():
                return Response({'error': 'Пользователь не имеет доступ к данному продукту'}, status=status.HTTP_403_FORBIDDEN)

            lessons = Lesson.objects.filter(product=product)
            lesson_serializer = LessonSerializer(lessons, many=True)
            return Response(lesson_serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

    def update_watched_status(self):
        # here, implement the logic to determine the "Viewed" status based on the percentage of views
        if self.watched_percentage >= 80:
            self.watched = True
        else:
            self.watched = False
        self.save()



# this view will collect statistics on products
class ProductStatisticsView(APIView):
    def get(self, request):
        products = Product.objects.all()

        product_statistics = []
        total_users = User.objects.count()

        for product in products:
            product_data = {
                'product_id': product.id,
                'product_name': product.name,
                'total_lessons_viewed': Lesson.objects.filter(product=product).aggregate(total_lessons_viewed=Count('id'))['total_lessons_viewed'],
                'total_time_spent_minutes': Lesson.objects.filter(product=product).aggregate(total_time_spent_minutes=Coalesce(Sum('view_time_minutes'), 0, output_field=FloatField()))['total_time_spent_minutes'],
                'total_users_enrolled': User.objects.filter(products_access=product).count(),
                'percent_acquisition': Decimal(User.objects.filter(products_access=product).count() / total_users * 100).quantize(Decimal('0.00')),
            }

            product_statistics.append(product_data)

        return Response(product_statistics)
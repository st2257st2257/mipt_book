from django.urls import path

from .views import index_test_book


app_name = 'test'

urlpatterns = [
    path('book/', index_test_book),
]

from django.urls import path

from .views import \
    index_test_auth, \
    index_test_get, \
    index_test_register

app_name = 'test'

urlpatterns = [
    path('register/', index_test_register),
    path('auth/', index_test_auth),
    path('get/', index_test_get),
]

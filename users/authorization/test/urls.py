from django.urls import path

from .views import \
    index_test_auth, \
    index_test_get

app_name = 'test'

urlpatterns = [
    path('auth/', index_test_auth),
    path('get/', index_test_get),
]

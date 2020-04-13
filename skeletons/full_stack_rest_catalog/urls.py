from django.conf.urls import include, url

urlpatterns = [
    # other URLs
    url(r'^api/3/users/(?P<user_id>\d+)/${resource_name_plural}', include('${django_app}.api_urls')),
    # other URLs
]

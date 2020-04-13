from django.conf.urls import url

from ${view_namespace} import ${view_class_name}

urlpatterns = [
    url(r'^$', ${view_class_name}.as_view(), name='${view_reverse_url_name}'),
]

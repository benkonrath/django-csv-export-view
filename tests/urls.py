from django.conf.urls import url

from .views import FieldTestView, ManyToManyView, ManyToOneView

urlpatterns = [
    url(r'^fields/$', FieldTestView.as_view(), name='fields'),
    url(r'^many-to-many/$', ManyToManyView.as_view(), name='many-to-many'),
    url(r'^many-to-one/$', ManyToOneView.as_view(), name='many-to-one'),
]

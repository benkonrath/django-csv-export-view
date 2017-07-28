from django.conf.urls import url

from .views import FieldTestAllView, FieldTestView, ManyToManyView, ManyToOneView, OneToOneView, OverrideGetQuerysetView

urlpatterns = [
    url(r'^fields/$', FieldTestView.as_view(), name='fields'),
    url(r'^fields-all/$', FieldTestAllView.as_view(), name='fields-all'),
    url(r'^many-to-many/$', ManyToManyView.as_view(), name='many-to-many'),
    url(r'^many-to-one/$', ManyToOneView.as_view(), name='many-to-one'),
    url(r'^one-to-one/$', OneToOneView.as_view(), name='one-to-one'),
    url(r'^override-get-queryset/$', OverrideGetQuerysetView.as_view(), name='override-get-queryset'),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.test import TestCase

from csv_export.views import CSVExportView

from .models import Car, FieldTest, Manufacturer, Pizza, Place, Restaurant, Topping

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse  # Django < 1.10


class CSVExportTests(TestCase):

    def test_unicode_field_value(self):
        pizza = Pizza.objects.create(name='Honoré')
        view = CSVExportView(fields='__all__')
        self.assertEqual(pizza.name, view.get_field_value(pizza, 'name'))

    def test_fields(self):
        date = datetime.date(2017, 1, 1)
        datetime_ = pytz.timezone('Europe/Amsterdam').localize(datetime.datetime(2017, 1, 1, 10, 0), is_dst=None)
        FieldTest.objects.create(date=date, datetime=datetime_)

        response = self.client.get(reverse('fields'))
        self.assertEqual(response.content.decode().strip(),
                         'sep=,\r\n"Date","Datetime","Choice","Empty Choice","My Property"\r\n"2017-01-01","2017-01-01 09:00:00+00:00","Red","","Foo"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="field-tests.csv"')

        # Using fields = '__all__' doesn't include properties.
        response = self.client.get(reverse('fields-all'))
        self.assertEqual(response.content.decode().strip(),
                         'sep=,\r\n"Id","Date","Datetime","Choice","Empty Choice"\r\n"1","2017-01-01","2017-01-01 09:00:00+00:00","Red",""')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="field-tests.csv"')

    def test_many_to_one(self):
        bmw = Manufacturer.objects.create(name='BMW')
        Car.objects.create(name='i3', manufacturer=bmw)

        response = self.client.get(reverse('many-to-one'))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"i3","BMW"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="cars.csv"')

    def test_many_to_many(self):
        pizza = Pizza.objects.create(name='Hawaiian')
        pizza.toppings.add(Topping.objects.create(name='Pineapple', code='P'))
        pizza.toppings.add(Topping.objects.create(name='Ham', code='H'))
        pizza.toppings.add(Topping.objects.create(name='Cheese', code='C'))

        response = self.client.get(reverse('many-to-many'))
        self.assertEqual(response.content.decode().strip(),
                         'sep=,\r\n"Name","Toppings","Topping Codes"\r\n"Hawaiian","Pineapple,Ham,Cheese","P,H,C"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="pizzas.csv"')

    def test_one_to_one(self):
        place = Place.objects.create(name='Jollibee', address='Manila')
        Restaurant.objects.create(place=place, serves_hot_dogs=True, serves_pizza=False)

        response = self.client.get(reverse('one-to-one'))
        self.assertEqual(response.content.decode().strip(),
                         'sep=,\r\n"Name","Address","Serves Hot Dogs","Serves Pizza"\r\n"Jollibee","Manila","True","False"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="places.csv"')

    def test_override_get_queryset(self):
        bmw = Manufacturer.objects.create(name='BMW')
        Car.objects.create(name='i3', manufacturer=bmw)

        toyota = Manufacturer.objects.create(name='Toyota')
        Car.objects.create(name='Yaris', manufacturer=toyota)

        response = self.client.get(reverse('override-get-queryset'))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"Yaris","Toyota"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="cars.csv"')

    def test_override_get_fields(self):
        bmw = Manufacturer.objects.create(name='BMW')
        Car.objects.create(name='i3', manufacturer=bmw)

        response = self.client.get(reverse('override-get-fields'))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name"\r\n"i3"')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="cars.csv"')

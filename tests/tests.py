import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from csv_export.views import CSVExportView

from .admin import CarAdmin
from .models import Car, FieldTest, Manufacturer, Pizza, Place, Restaurant, Topping


class CSVExportTests(TestCase):
    def test_unicode_field_value(self):
        pizza = Pizza.objects.create(name="Honoré")
        view = CSVExportView(fields="__all__")
        self.assertEqual(pizza.name, view.get_field_value(pizza, "name"))

    def test_fields(self):
        date = datetime.date(2017, 1, 1)
        datetime_ = datetime.datetime(2017, 1, 1, 10, 0, tzinfo=ZoneInfo("Europe/Amsterdam"))
        FieldTest.objects.create(date=date, datetime=datetime_)

        response = self.client.get(reverse("fields"))
        self.assertEqual(
            response.content.decode().strip(),
            'sep=,\r\n"Date","Datetime","Choice","Empty Choice","Integer Choice","My Property"\r\n'
            '"2017-01-01","2017-01-01 09:00:00+00:00","Red","","Zero","Foo"',
        )
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="field-tests.csv"')

        # Using fields = '__all__' doesn't include properties.
        response = self.client.get(reverse("fields-all"))
        self.assertEqual(
            response.content.decode().strip(),
            'sep=,\r\n"Id","Date","Datetime","Choice","Empty Choice","Integer Choice"\r\n'
            '"1","2017-01-01","2017-01-01 09:00:00+00:00","Red","","Zero"',
        )
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="field-tests.csv"')

    def test_verbose_names(self):
        response = self.client.get(reverse("verbose-names"))
        self.assertEqual(
            response.content.decode().strip(),
            'sep=,\r\n"id","date","datetime","choice","empty_choice","integer_choice"',
        )

    def test_many_to_one(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        response = self.client.get(reverse("many-to-one"))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"i3","BMW"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    def test_many_to_many(self):
        pizza = Pizza.objects.create(name="Hawaiian")
        pizza.toppings.add(Topping.objects.create(name="Pineapple", code="P"))
        pizza.toppings.add(Topping.objects.create(name="Ham", code="H"))
        pizza.toppings.add(Topping.objects.create(name="Cheese", code="C"))

        response = self.client.get(reverse("many-to-many"))
        self.assertEqual(
            response.content.decode().strip(),
            'sep=,\r\n"Name","Toppings","Topping Codes"\r\n"Hawaiian","Pineapple,Ham,Cheese","P,H,C"',
        )
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="pizzas.csv"')

    def test_one_to_one(self):
        place = Place.objects.create(name="Jollibee", address="Manila")
        Restaurant.objects.create(place=place, serves_hot_dogs=True, serves_pizza=False)

        response = self.client.get(reverse("one-to-one"))
        self.assertEqual(
            response.content.decode().strip(),
            'sep=,\r\n"Name","Address","Serves Hot Dogs","Serves Pizza"\r\n"Jollibee","Manila","True","False"',
        )
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="places.csv"')

    def test_override_get_queryset(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        toyota = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(name="Yaris", manufacturer=toyota)

        response = self.client.get(reverse("override-get-queryset"))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"Yaris","Toyota"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    def test_override_get_fields(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        response = self.client.get(reverse("override-get-fields"))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name"\r\n"i3"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    @parameterized.expand(["set-filename", "override-get-filename"])
    def test_filename(self, view_name):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        response = self.client.get(reverse(view_name))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Id","Name","Manufacturer"\r\n"1","i3","BMW"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="fancy-cars.csv"')

    def test_override_get_csv_writer_fmtparams(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        response = self.client.get(reverse("override-get-csv-writer-fmtparams"))
        self.assertEqual(response.content.decode().strip(), 'sep=|\r\n"Name"|"Manufacturer"\r\n"i3"|"BMW"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    def test_admin_csv_export(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        car_admin = CarAdmin(Car, None)
        response = car_admin.export_car_csv(None, Car.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Id","Name","Manufacturer"\r\n"1","i3","BMW"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    def test_unicode_csv_data(self):
        schrodinger = Manufacturer.objects.create(name="Schrödinger")
        Car.objects.create(name="Cat", manufacturer=schrodinger)

        response = self.client.get(reverse("many-to-one"))
        self.assertEqual(
            response.content.decode("utf-8").strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"Cat","Schrödinger"'
        )
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

    def test_improperly_configured(self):
        # get_context_data()
        class OverrideGetContextDataView(CSVExportView):
            fields = "__all__"

            def get_context_data(self, **kwargs):
                return super(OverrideGetContextDataView, self).get_context_data()

        with self.assertRaises(ImproperlyConfigured) as cm:
            OverrideGetContextDataView()
        self.assertEqual(cm.exception.args[0], "Overriding 'get_context_data()' is not permitted.")

        # get_paginate_by()
        class OverrideGetPaginateByView(CSVExportView):
            fields = "__all__"

            def get_paginate_by(self, queryset):
                return super(OverrideGetPaginateByView, self).get_paginate_by(queryset)

        with self.assertRaises(ImproperlyConfigured) as cm:
            OverrideGetPaginateByView()
        self.assertEqual(cm.exception.args[0], "Overriding 'get_paginate_by()' is not permitted.")

        # get_allow_empty()
        class OverrideGetAllowEmptyView(CSVExportView):
            fields = "__all__"

            def get_allow_empty(self):
                return super(OverrideGetAllowEmptyView, self).get_allow_empty()

        with self.assertRaises(ImproperlyConfigured) as cm:
            OverrideGetAllowEmptyView()
        self.assertEqual(cm.exception.args[0], "Overriding 'get_allow_empty()' is not permitted.")

        # get_context_object_name()
        class OverrideGetContextObjectNameView(CSVExportView):
            fields = "__all__"

            def get_context_object_name(self, object_list):
                return super(OverrideGetContextObjectNameView, self).get_context_object_name(object_list)

        with self.assertRaises(ImproperlyConfigured) as cm:
            OverrideGetContextObjectNameView()
        self.assertEqual(cm.exception.args[0], "Overriding 'get_context_object_name()' is not permitted.")

        # paginate_by
        with self.assertRaises(ImproperlyConfigured) as cm:
            CSVExportView(fields="__all__", paginate_by=10)
        self.assertEqual(cm.exception.args[0], "'CSVExportView' does not support pagination.")

        # allow_empty
        with self.assertRaises(ImproperlyConfigured) as cm:
            CSVExportView(fields="__all__", allow_empty=False)
        self.assertEqual(cm.exception.args[0], "'CSVExportView' does not support disabling allow_empty.")

        # context_object_name
        with self.assertRaises(ImproperlyConfigured) as cm:
            CSVExportView(fields="__all__", context_object_name="foo")
        self.assertEqual(cm.exception.args[0], "'CSVExportView' does not support setting context_object_name.")

    def test_related_uses_model_str(self):
        bmw = Manufacturer.objects.create(name="BMW")
        Car.objects.create(name="i3", manufacturer=bmw)

        response = self.client.get(reverse("related-uses-model-str"))
        self.assertEqual(response.content.decode().strip(), 'sep=,\r\n"Name","Manufacturer"\r\n"i3","BMW"')
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="cars.csv"')

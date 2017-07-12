from csv_export.views import CSVExportView

from .models import Car, FieldTest, Pizza


class FieldTestView(CSVExportView):
    model = FieldTest


class ManyToOneView(CSVExportView):
    model = Car
    fields = ('name', 'manufacturer__name')

    def get_header_name(self, model, field_name):
        if field_name == 'manufacturer__name':
            return 'Manufacturer'
        return super(ManyToOneView, self).get_header_name(model, field_name)


class ManyToManyView(CSVExportView):
    model = Pizza
    fields = ('name', 'toppings')

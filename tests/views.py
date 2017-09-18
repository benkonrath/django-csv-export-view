from csv_export.views import CSVExportView

from .models import Car, FieldTest, Pizza, Place


class FieldTestView(CSVExportView):
    model = FieldTest
    fields = ('date', 'datetime', 'choice', 'empty_choice', 'my_property')


class FieldTestAllView(CSVExportView):
    model = FieldTest
    fields = '__all__'


class ManyToOneView(CSVExportView):
    model = Car
    fields = ('name', 'manufacturer__name')

    def get_header_name(self, model, field_name):
        if field_name == 'manufacturer__name':
            return 'Manufacturer'
        return super(ManyToOneView, self).get_header_name(model, field_name)


class ManyToManyView(CSVExportView):
    model = Pizza
    fields = ('name', 'toppings', 'toppings__code')

    def get_header_name(self, model, field_name):
        if field_name == 'toppings__code':
            return 'Topping Codes'
        return super(ManyToManyView, self).get_header_name(model, field_name)


class OneToOneView(CSVExportView):
    model = Place
    fields = ('name', 'address', 'restaurant__serves_hot_dogs', 'restaurant__serves_pizza')


class OverrideGetQuerysetView(ManyToOneView):
    def get_queryset(self):
        queryset = super(OverrideGetQuerysetView, self).get_queryset()
        return queryset.filter(manufacturer__name='Toyota')


class OverrideGetFieldsView(CSVExportView):
    model = Car

    def get_fields(self, queryset):
        fields = ['name', 'manufacturer__name']
        if not self.request.user.is_superuser:
            fields.remove('manufacturer__name')
        return fields


class OverrideGetCSVWriterFmtParamsView(ManyToOneView):
    def get_csv_writer_fmtparams(self):
        fmtparams = super(OverrideGetCSVWriterFmtParamsView, self).get_csv_writer_fmtparams()
        fmtparams['delimiter'] = '|'
        return fmtparams


class OverrideGetContextDataView(CSVExportView):
    def get_context_data(self):
        context = super(OverrideGetContextDataView, self).get_context_data()
        context['sport'] = 'baseball'
        return context

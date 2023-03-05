from csv_export.views import CSVExportView

from .models import Car, FieldTest, Pizza, Place


class FieldTestView(CSVExportView):
    model = FieldTest
    fields = ("date", "datetime", "choice", "empty_choice", "integer_choice", "my_property")


class FieldTestAllView(CSVExportView):
    model = FieldTest
    fields = "__all__"


class VerboseNamesView(CSVExportView):
    model = FieldTest
    fields = "__all__"
    verbose_names = False


class ManyToOneView(CSVExportView):
    model = Car
    fields = ("name", "manufacturer__name")

    def get_header_name(self, model, field_name):
        if field_name == "manufacturer__name":
            return "Manufacturer"
        return super().get_header_name(model, field_name)


class ManyToManyView(CSVExportView):
    model = Pizza
    fields = ("name", "toppings", "toppings__code")

    def get_header_name(self, model, field_name):
        if field_name == "toppings__code":
            return "Topping Codes"
        return super().get_header_name(model, field_name)


class OneToOneView(CSVExportView):
    model = Place
    fields = ("name", "address", "restaurant__serves_hot_dogs", "restaurant__serves_pizza")


class OverrideGetQuerysetView(ManyToOneView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(manufacturer__name="Toyota")


class OverrideGetFieldsView(CSVExportView):
    model = Car

    def get_fields(self, queryset):
        fields = ["name", "manufacturer__name"]
        if not self.request.user.is_superuser:
            fields.remove("manufacturer__name")
        return fields


class SetFilenameView(CSVExportView):
    model = Car
    filename = "fancy-cars.csv"


class OverrideGetFilenameView(CSVExportView):
    model = Car

    def get_filename(self, queryset):
        return "fancy-cars.csv"


class OverrideGetCSVWriterFmtParamsView(ManyToOneView):
    def get_csv_writer_fmtparams(self):
        fmtparams = super().get_csv_writer_fmtparams()
        fmtparams["delimiter"] = "|"
        return fmtparams


class RelatedUsesModelStrView(CSVExportView):
    model = Car
    fields = ("name", "manufacturer")

    def get_queryset(self):
        return super().get_queryset().select_related("manufacturer")

# django-csv-export-view

A Django class-based view for CSV export.

[![Build Status](https://travis-ci.org/benkonrath/django-csv-export-view.svg?branch=master)](https://travis-ci.org/benkonrath/django-csv-export-view)

## Features

* Easy CSV exports by setting a Django `model` and a `fields` or `exclude` iterable
* Works with existing class-based view mixins for access control
* Generates Microsoft Excel friendly CSV by default
* Proper HTTP headers set for CSV
* Easy to override defaults as needed
* Easy integration into Django Admin

## Installation

`pip install django-csv-export-view`

## Quick Start

Examples:
```python
from csv_export.views import CSVExportView

class DataExportView(CSVExportView):
    model = Data
    fields = ("field", "related", "property")

    # When using related fields you will likely want to override get_queryset() use select_related() or prefetch_related().
    def get_queryset(self):
        return super().get_queryset().select_related("related")
        OR
        return super().get_queryset().prefetch_related("related")

class DataExportView(CSVExportView):
    model = Data
    fields = ("field", "related__field", "property")

class DataExportView(CSVExportView):
    model = Data
    fields = "__all__"

class DataExportView(CSVExportView):
    model = Data
    exclude = ("id",)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(deleted=True)

class DataExportView(CSVExportView):
    model = Data

    def get_fields(self, queryset):
        fields = ["username", "email"]
        if self.request.user.is_superuser:
            fields.append("birth_date")
        return fields
```

`fields` / `exclude`: An iterable of field names and properties. You cannot set both `fields` and `exclude`.
`fields` can also be `"__all__"` to export all fields. Model properties are not included when `"__all__"` is used.
Related field can be used with `__`. Override `get_fields(self, queryset)` for custom behaviour not supported by the
default logic.

`model`: The model to use for the CSV export queryset. Override `get_queryset()` if you need a custom queryset.

## Further Customization

Examples:
```python
from csv_export.views import CSVExportView

class DataExportView(CSVExportView):
    model = Data
    fields = "__all__"
    header = False
    specify_separator = False
    filename = "data-export.csv"

class DataExportView(CSVExportView):
    model = Data
    fields = "__all__"
    verbose_names = False

class DataExportView(CSVExportView):
    model = Data
    fields = "__all__"

    def get_filename(self, queryset):
        return "data-export-{!s}.csv".format(timezone.now())
```

`header` - *boolean* - Default: `True`  
Whether to include the header in the CSV.

`filename` - *string* - Default: Dasherized version of `verbose_name_plural` from `queryset.model`.  
Override `get_filename(self, queryset)` if a dynamic filename is required.

`specify_separator` - *boolean* - Default: `True`  
Whether to include `sep=<sepaator>` as the first line of the CSV file. This is useful for generating Microsoft
Excel friendly CSV.

`verbose_names` - *boolean* - Default: `True`  
Whether to use capitalized verbose column names in the header of the CSV file. If `False`, field names are used
instead.

## CSV Writer Options

Example:
```python
from csv_export.views import CSVExportView

class DataExportView(CSVExportView):
    model = Data
    fields = "__all__"

    def get_csv_writer_fmtparams(self):
        fmtparams = super().get_csv_writer_fmtparams()
        fmtparams["delimiter"] = "|"
        return fmtparams
```

Override `get_csv_writer_fmtparams(self)` and return a dictionary of csv write format parameters. Default format
parameters are: dialect="excel" and quoting=csv.QUOTE_ALL. See all available options in the Python docs:

https://docs.python.org/3.9/library/csv.html#csv.writer

## Django Admin Integration

Example:
```python
from django.contrib import admin
from csv_export.views import CSVExportView

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    actions = ("export_data_csv",)

    def export_data_csv(self, request, queryset):
        view = CSVExportView(queryset=queryset, fields="__all__")
        return view.get(request)

    export_data_csv.short_description = "Export CSV for selected Data records"
```

## Contributions

Pull requests are happily accepted.

## Alternatives

https://github.com/django-import-export/django-import-export/

https://github.com/mjumbewu/django-rest-framework-csv

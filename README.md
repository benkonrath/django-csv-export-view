# django-csv-export-view

A Django class-based view for CSV export.

[![Build Status](https://travis-ci.org/benkonrath/django-csv-export-view.svg?branch=master)](https://travis-ci.org/benkonrath/django-csv-export-view)

## Features

* Easy CSV exports using the familiar `model` and `fields` / `exclude` pattern
* Works with your existing class-based view mixins for access control
* Generates Micosoft Excel friendly CSV by default
* Easy to override defaults as needed
* Proper HTTP headers set for CSV

## Quick Start

Examples:
```python
class DataExportView(CSVExportView):
    model = Data
    fields = ('field1', 'field2__related_field', 'property1')

class DataExportView(CSVExportView):
    model = Data
    fields = '__all__'

class DataExportView(CSVExportView):
    exclude = ('id',)

    def get_queryset(self):
        queryset = super(DataExportView, self).get_queryset()
        return queryset.filter(deleted=True)

class DataExportView(CSVExportView):
    model = Data

    def get_fields(self, queryset):
        fields = ['username', 'email']
        if self.request.user.is_superuser:
            fields.append('birth_date')
        return fields
```

`fields` / `exclude`: An interable of field names and properties. You cannot set both `fields` and `exclude`.
`fields` can also be `'__all__'` to export all fields. Model properties are not included when `'__all__'` is used.
Related field can be used with `__`. Override `get_fields(self, queryset)` for custom behaviour not supported by the
default logic.

`model`: The model to use for the CSV export queryset. Override `get_queryset()` if you need a custom queryset.

## Further Customization

Examples:
```python
class DataExportView(CSVExportView):
    model = Data
    fields = '__all__'
    header = False
    specify_separator = False
    filename = 'data-export.csv'

class DataExportView(CSVExportView):
    model = Data
    fields = '__all__'

    def get_filename(self, queryset):
        return 'data-export-{!s}.csv'.format(timezone.now())
```

`header` - *boolean* - Default: `True`  
Whether or not to include the header in the CSV.

`filename` - *string* - Default: Dasherized version of `verbose_name_plural` from `queryset.model`.  
Override `get_filename(self, queryset)` if a dynamic filename is required.

`specify_separator` - *boolean* - Default: `True`  
Whether or not to include `sep=<sepaator>` as the first line of the CSV file. This is useful for generating Microsoft
Excel friendly CSV.

## Contributions

Pull requests are happily accepted.

## Alternatives

https://github.com/django-import-export/django-import-export/

https://github.com/mjumbewu/django-rest-framework-csv

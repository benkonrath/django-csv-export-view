import csv

from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponse
from django.views.generic.base import View


class CSVView(View):
    model = None
    queryset = None
    fields = None
    exclude = None
    header = True
    dialect = 'excel'
    specify_separator = True  # Useful for Excel.
    filename = None

    http_method_names = ('get',)

    def __init__(self, **kwargs):
        super(CSVView, self).__init__(**kwargs)

        if self.fields and self.exclude:
            raise ImproperlyConfigured('\'{0}\' cannot set fields and excludes.'.format(self.__class__.__name__))

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may be a queryset (in which qs-specific
        behavior will be enabled).

        This method was taken from django.views.generic.list.MultipleObjectMixin.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured("'{0}' must define 'queryset' or 'model'".format(self.__class__.__name__))
        return queryset

    def get_fields(self, queryset):
        """ Override if a dynamic fields are required. """
        field_names = self.fields
        if not self.fields:
            opts = queryset.model._meta
            field_names = [field.name for field in opts.fields]
        return field_names

    def get_filename(self, queryset):
        """ Override if a dynamic filename is required. """
        filename = self.filename
        if not filename:
            opts = queryset.model._meta
            filename = unicode(opts).replace('.', '_')
        return filename

    def get_field_value(self, obj, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        if '__' not in field_name:
            value = getattr(obj, field_name)
            if value is None:
                return ''

            # Datetime field.
            if hasattr(value, 'isoformat') and hasattr(value.isoformat, '__call__'):
                return value.isoformat()

            # Django country field.
            if hasattr(value, 'code') and hasattr(value, 'flag'):
                return value.code

            # Choice field.
            choices_function_name = 'get_{0}_display'.format(field_name)
            if hasattr(obj, choices_function_name):
                choices_function = getattr(obj, choices_function_name)
                if hasattr(choices_function, '__call__'):
                    return choices_function()

            return unicode(value).encode('utf-8', 'replace')
        else:
            related_field_names = field_name.split('__')
            related_obj = getattr(obj, related_field_names[0])
            related_field_name = '__'.join(related_field_names[1:])
            return self.get_field_value(related_obj, related_field_name)

    def get_field_name(self, model, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        opts = model._meta
        if '__' not in field_name:
            return unicode(opts.get_field(field_name).verbose_name).encode('utf-8', 'replace').capitalize()
        else:
            related_field_names = field_name.split('__')

            field_object, model, direct, m2m = opts.get_field_by_name(related_field_names[0])
            if hasattr(field_object, 'rel'):
                related_model = field_object.rel.to
            else:
                # field_object should be instance of RelatedObject
                related_model = field_object.model

            related_field_name = '__'.join(related_field_names[1:])
            return self.get_field_name(related_model, related_field_name)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        field_names = self.get_fields(queryset)

        if self.exclude:
            # Note: Ordering is undefined in this case.
            exclude_set = set(self.exclude)
            field_names = list(set(field_names) - exclude_set)

        response = HttpResponse(content_type='text/csv')

        filename = self.get_filename(queryset)
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(filename)

        writer = csv.writer(response, dialect=self.dialect, quoting=csv.QUOTE_ALL)

        if self.specify_separator:
            response.write('sep={0}{1}'.format(writer.dialect.delimiter, writer.dialect.lineterminator))

        if self.header:
            writer.writerow([self.get_field_name(queryset.model, field_name) for field_name in list(field_names)])

        for obj in queryset:
            writer.writerow([self.get_field_value(obj, field) for field in field_names])
        return response

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.http.response import HttpResponse
from django.utils import six
from django.utils.encoding import force_text
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin


class CSVExportView(MultipleObjectMixin, View):
    fields = None
    exclude = None
    header = True
    dialect = 'excel'
    specify_separator = True  # Useful for Excel.
    filename = None

    # Override some defaults.
    paginate_by = None
    paginator_class = None
    page_kwarg = None
    allow_empty = True
    context_object_name = None

    def __init__(self, **kwargs):
        super(CSVExportView, self).__init__(**kwargs)

        if self.fields and self.exclude:
            raise ImproperlyConfigured('\'{}\' cannot set fields and excludes.'.format(self.__class__.__name__))

    def get_paginate_by(self, queryset):
        if self.paginate_by:
            raise ImproperlyConfigured('\'{}\' does not support pagination.'.format(self.__class__.__name__))
        return None

    def get_allow_empty(self):
        if not self.allow_empty:
            raise ImproperlyConfigured('\'{}\' does not support disabling allow_empty.'.format(self.__class__.__name__))
        return True

    def get_context_object_name(self, object_list):
        if self.context_object_name:
            raise ImproperlyConfigured('\'{}\' does not support setting context_object_name.'.format(self.__class__.__name__))
        return None

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
            filename = six.text_type(opts).replace('.', '_')
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
            choices_function_name = 'get_{}_display'.format(field_name)
            if hasattr(obj, choices_function_name):
                choices_function = getattr(obj, choices_function_name)
                if hasattr(choices_function, '__call__'):
                    return choices_function()

            return force_text(value)
        else:
            related_field_names = field_name.split('__')
            related_obj = getattr(obj, related_field_names[0])
            related_field_name = '__'.join(related_field_names[1:])
            return self.get_field_value(related_obj, related_field_name)

    def get_field_name(self, model, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        opts = model._meta
        if '__' not in field_name:
            try:
                field = opts.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(model, field_name):
                    raise e
                # field_name is most likely a property.
                return field_name.replace('_', ' ').title()

            return force_text(field.verbose_name).title()
        else:
            related_field_names = field_name.split('__')
            field = opts.get_field(related_field_names[0])
            assert field.is_relation
            return self.get_field_name(field.related_model, '__'.join(related_field_names[1:]))

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        field_names = self.get_fields(queryset)

        if self.exclude:
            # Note: Ordering is undefined in this case.
            exclude_set = set(self.exclude)
            field_names = list(set(field_names) - exclude_set)

        response = HttpResponse(content_type='text/csv')

        filename = self.get_filename(queryset)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

        writer = csv.writer(response, dialect=self.dialect, quoting=csv.QUOTE_ALL)

        if self.specify_separator:
            response.write('sep={}{}'.format(writer.dialect.delimiter, writer.dialect.lineterminator))

        if self.header:
            writer.writerow([self.get_field_name(queryset.model, field_name) for field_name in list(field_names)])

        for obj in queryset:
            writer.writerow([self.get_field_value(obj, field) for field in field_names])
        return response

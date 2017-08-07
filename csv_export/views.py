# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.http.response import HttpResponse
from django.utils import six
from django.utils.encoding import force_text
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin


def _get_method_type():
    class C(object):
        def x(self):
            pass
    return type(getattr(C, 'x'))

_method_type = _get_method_type()



class CSVExportView(MultipleObjectMixin, View):
    fields = None
    exclude = None
    header = True
    specify_separator = True  # Useful for Excel.
    filename = None

    # Override some View defaults that are not supported by CSVExportView.
    paginate_by = None
    paginator_class = None
    page_kwarg = None
    allow_empty = True
    context_object_name = None

    def __init__(self, **kwargs):
        super(CSVExportView, self).__init__(**kwargs)

        # Only check if fields / excludes are setup correctly when get_fields is not overridden.
        get_fields_overridden = False
        for cls in self.__class__.__mro__:
            if cls == CSVExportView:
                break
            if hasattr(cls, 'get_fields') and type(getattr(cls, 'get_fields')) == _method_type:
                get_fields_overridden = True
                break

        if not get_fields_overridden:
            if not self.fields and not self.exclude:
                raise ImproperlyConfigured("'fields' or 'exclude' must be specified.")

            if self.fields and self.exclude:
                raise ImproperlyConfigured("Specifying both 'fields' and 'exclude' is not permitted.")

        # TODO Check to see that get_context_data() is not being overridden.

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
        if not field_names or field_names == '__all__':
            opts = queryset.model._meta
            field_names = [field.name for field in opts.fields]

        if self.exclude:
            # Note: Ordering is undefined in this case.
            exclude_set = set(self.exclude)
            field_names = list(set(field_names) - exclude_set)

        return field_names

    def get_filename(self, queryset):
        """ Override if a dynamic filename is required. """
        filename = self.filename
        if not filename:
            filename = queryset.model._meta.verbose_name_plural.replace(' ', '-')
        return filename

    def get_field_value(self, obj, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        if '__' not in field_name:
            if hasattr(obj, 'all') and hasattr(obj, 'iterator'):
                return ','.join([getattr(ro, field_name) for ro in obj.all()])

            try:
                field = obj._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(obj, field_name):
                    raise e
                # field_name is a property.
                return getattr(obj, field_name)

            value = field.value_from_object(obj)
            if field.many_to_many:
                return ','.join([six.text_type(ro) for ro in value])
            elif field.choices:
                if not value:
                    return ''
                return dict(field.choices)[value]
            return field.value_from_object(obj)
        else:
            related_field_names = field_name.split('__')
            related_obj = getattr(obj, related_field_names[0])
            related_field_name = '__'.join(related_field_names[1:])
            return self.get_field_value(related_obj, related_field_name)

    def get_header_name(self, model, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        if '__' not in field_name:
            try:
                field = model._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(model, field_name):
                    raise e
                # field_name is a property.
                return field_name.replace('_', ' ').title()

            return force_text(field.verbose_name).title()
        else:
            related_field_names = field_name.split('__')
            field = model._meta.get_field(related_field_names[0])
            assert field.is_relation
            return self.get_header_name(field.related_model, '__'.join(related_field_names[1:]))

    def get_csv_writer_fmtparams(self):
        return {
            'dialect': 'excel',
            'quoting': csv.QUOTE_ALL,
        }

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        field_names = self.get_fields(queryset)

        response = HttpResponse(content_type='text/csv')

        filename = self.get_filename(queryset)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

        writer = csv.writer(response, **self.get_csv_writer_fmtparams())

        if self.specify_separator:
            response.write('sep={}{}'.format(writer.dialect.delimiter, writer.dialect.lineterminator))

        if self.header:
            writer.writerow([self.get_header_name(queryset.model, field_name) for field_name in list(field_names)])

        for obj in queryset:
            writer.writerow([self.get_field_value(obj, field) for field in field_names])

        return response

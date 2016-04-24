# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .views import CSVExportView


class CSVExportTests(TestCase):

    def test_unicode_field_value(self):
        class DataObject(object):
            name = 'Honoré'

        obj = DataObject()
        view = CSVExportView()
        view.get_field_value(obj, 'name')

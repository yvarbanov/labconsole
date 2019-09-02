import os

from .models import LabConsole
from .database import info
from django.test import TestCase

# These basic tests are to be used as an example for running tests in S2I
# and OpenShift when building an application image.
class LabConsoleModelTest(TestCase):
    def test_viewlabconsole_model(self):
        labconsoleview = LabConsole.objects.create(hostname='localhost')
        labconsoletest = LabConsole.objects.get(hostname='localhost')
        self.assertEqual(labconsoletest.hostname, 'localhost')

class LabConsoleTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


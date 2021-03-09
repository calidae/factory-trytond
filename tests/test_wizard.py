import unittest.mock

from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class WizardTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @with_transaction()
    def test_create_wizard(self):
        """Create a wizard."""

        class WizardFactory(factory_trytond.WizardFactory):
            class Meta:
                model = 'test.test_wizard'

        WizardModel = Pool().get('test.test_wizard', type='wizard')
        wizard = WizardFactory.create()
        self.assertTrue(isinstance(wizard, WizardModel))

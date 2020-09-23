import unittest

import factory

from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class ModelDataTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('ir')

    @with_transaction()
    def test_model_data(self):
        pool = Pool()
        Lang = pool.get('ir.lang')
        Menu = pool.get('ir.ui.menu')

        class StubFactory(factory.StubFactory):
            english = factory_trytond.ModelData('ir', 'lang_en')
            admin = factory_trytond.ModelData('ir', 'menu_administration')

        stub = StubFactory.build()

        self.assertIsInstance(stub.english, Lang)
        self.assertEqual(stub.english.name, 'English')

        self.assertIsInstance(stub.admin, Menu)
        self.assertEqual(stub.admin.name, 'Administration')

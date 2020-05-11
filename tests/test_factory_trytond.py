import unittest

import factory

from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class RemoveMeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @with_transaction()
    def test_yes(self):
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        model = ModelFactory.create()

        self.assertEqual(
            Model.search([]),
            [model]
        )

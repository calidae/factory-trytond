import unittest.mock

import factory

from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class FactoryTrytondTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @with_transaction()
    def test_named_metamodel(self):
        """Declare a factory declaring the meta-model by name"""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        record = ModelFactory.create()

        self.assertEqual(Model.search([]), [record])

    @with_transaction()
    def test_build(self):
        """Test that build strategy won't persist records"""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        ModelFactory.build()
        self.assertFalse(Model.search([]))

    @with_transaction()
    def test_create_set_attribute(self):
        """Create an object with a given name."""

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        record = ModelFactory.create(name='foo')
        self.assertEqual(record.name, 'foo')

    @with_transaction()
    def test_create_batch_faker(self):
        """Create multiple objects with auto-generated names."""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        records = ModelFactory.create_batch(5)

        self.assertEqual(Model.search([]), records)

    @with_transaction()
    def test_create_batch_set_attribute(self):
        """Create multiple objects with a given name."""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        ModelFactory.create_batch(5, name=factory.Iterator(list('abcde')))

        self.assertCountEqual(
            [record.name for record in Model.search([])],
            list('abcde')
        )

    @with_transaction()
    def test_on_change(self):
        """Test that a factory classmethod on_change
        will be called with the new instance"""

        sentinel = unittest.mock.sentinel

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

            @classmethod
            def on_change(cls, obj):
                sentinel.obj = obj

        record = ModelFactory.create()
        self.assertIs(sentinel.obj, record)

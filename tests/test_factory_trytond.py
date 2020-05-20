import unittest

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
    def test_create_faker(self):
        """Create an object with an auto-generated name."""
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

    @with_transaction()
    def test_create_set_attribute(self):
        """Create an object with a given name."""

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        model = ModelFactory.create(name='Foo')

        self.assertEqual(model.name, 'Foo')

    @with_transaction()
    def test_create_batch_faker(self):
        """Create multiple objects with auto-generated names."""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        models = []
        models.extend(ModelFactory.create_batch(5))

        self.assertEqual(
            Model.search([]),
            models
        )

    @with_transaction()
    def test_create_batch_set_attribute(self):
        """Create multiple objects with a given name."""
        Model = Pool().get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        models = []
        models.extend(ModelFactory.create_batch(5, name='Foo'))

        self.assertEqual(
            Model.search([]),
            models
        )

    @with_transaction()
    def test_subfactory_create(self):
        """Create an object with a related parent."""
        Model = Pool().get('test.mptt')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Parent'

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Child'
            parent = factory.SubFactory(ModelFactory)

        model_child = ModelChildFactory.create()

        self.assertEqual(
            Model.search([('name', '=', 'Child')]),
            [model_child]
        )

    @with_transaction()
    def test_subfactory_batch(self):
        """Create multiple objects with a related parent."""
        Model = Pool().get('test.mptt')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Parent'

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Child'
            parent = factory.SubFactory(ModelFactory)

        model_childs = []
        model_childs.extend(ModelChildFactory.create_batch(3))

        self.assertEqual(
            Model.search([('name', '=', 'Child')]),
            model_childs
        )

    @with_transaction()
    def test_relatedfactorylist_create(self):
        """Create an object with related childs."""
        Model = Pool().get('test.mptt')

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Child'

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Parent'
            childs = factory.RelatedFactoryList(
                ModelChildFactory,
                factory_related_name='parent',
                size=2
            )

        model = ModelFactory.create()

        self.assertEqual(
            Model.search([('name', '=', 'Parent')]),
            [model]
        )

    @with_transaction()
    def test_relatedfactorylist_batch(self):
        """Create multiple objects with related childs."""
        Model = Pool().get('test.mptt')

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Child'

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.mptt'
            name = 'Parent'
            childs = factory.RelatedFactoryList(
                ModelChildFactory,
                factory_related_name='parent',
                size=2
            )

        models = []
        models.extend(ModelFactory.create_batch(3))

        self.assertEqual(
            Model.search([('name', '=', 'Parent')]),
            models
        )

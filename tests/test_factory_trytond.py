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
        Model = Pool().get('test.model')

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
        """Create an object with a parent from a SubFactory."""
        ModelChild = Pool().get('test.model_child')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model_parent'
            name = factory.Faker('word')

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model_child'
            name = factory.Faker('word')
            parent = factory.SubFactory(ModelFactory)
        
        model_child = ModelChildFactory.create()
        
        self.assertEqual(
            ModelChild.search([]),
            [model_child]
        )

    @with_transaction()
    def test_subfactory_batch(self):
        """Create multiple objects, each with a parent from a SubFactory."""
        ModelChild = Pool().get('test.model_child')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model_parent'
            name = factory.Faker('word')

        class ModelChildFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model_child'
            name = factory.Faker('word')
            parent = factory.SubFactory(ModelFactory)

        model_childs = []
        model_childs.extend(ModelChildFactory.create_batch(5))

        self.assertEqual(
            ModelChild.search([]),
            model_childs
        )

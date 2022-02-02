import unittest.mock

import factory
import pytest

import factory_trytond


class AbstractStaticFactory(factory_trytond.TrytonFactory):
    class Meta:
        abstract = True


class StaticFactory(AbstractStaticFactory):
    class Meta:
        model = 'test.model'


class InheritedStaticFactory(StaticFactory):
    pass


class TestFactoryTrytond():

    def test_static_named_metamodel(self, pool):
        """Declare and inherit a static factory"""
        Model = pool.get('test.model')

        record1 = StaticFactory.create()
        record2 = InheritedStaticFactory.create()

        assert Model.search([]) == [record1, record2]

    def test_dynamic_named_metamodel(self, pool):
        """Declare and inherit a dynamic factory
        declaring the meta-model by name"""
        Model = pool.get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        class InheritedModelFactory(ModelFactory):
            pass

        record1 = ModelFactory.create()
        record2 = InheritedModelFactory.create()

        assert Model.search([]) == [record1, record2]

    def test_dynamic_pool_metamodel(self, pool):
        """Declare and inherit a dynamic factory
        declaring the meta-model with a pool model"""
        Model = pool.get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = Model

        class InheritedModelFactory(ModelFactory):
            pass

        record1 = ModelFactory.create()
        record2 = InheritedModelFactory.create()

        assert Model.search([]) == [record1, record2]

    def test_build(self, pool):
        """Test that build strategy won't persist records"""
        Model = pool.get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        ModelFactory.build()
        assert not Model.search([])

    @pytest.mark.usefixtures('transaction')
    def test_create_set_attribute(self):
        """Create an object with a given name."""

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        record = ModelFactory.create(name='foo')
        assert record.name == 'foo'

    def test_create_batch_faker(self, pool):
        """Create multiple objects with auto-generated names."""
        Model = pool.get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'
            name = factory.Faker('word')

        records = ModelFactory.create_batch(5)

        assert Model.search([]) == records

    def test_create_batch_set_attribute(self, pool):
        """Create multiple objects with a given name."""
        Model = pool.get('test.model')

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        ModelFactory.create_batch(5, name=factory.Iterator(list('abcde')))

        assert [record.name for record in Model.search([])] == list('abcde')

    @pytest.mark.usefixtures('transaction')
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
        assert sentinel.obj is record

import unittest

import factory

from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class LazySearchTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @with_transaction()
    def test_lazy_search(self):

        class ModelFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.model'

        class StubFactory(factory.StubFactory):
            name = 'foo'
            foo = factory_trytond.LazySearch(
                'test.model',
                lambda stub: [('name', '=', stub.name)],
            )
            first = factory_trytond.LazySearch(
                'test.model',
                lambda stub: [('name', '=', stub.name)],
                limit=1,
            )

        (foo1, foo2) = ModelFactory.create_batch(2, name='foo')
        bar = ModelFactory.create(name='bar')
        stubs = StubFactory.build_batch(10)

        self.assertEqual([stub.first for stub in stubs], [foo1] * 10)
        self.assertNotIn(bar, {stub.foo for stub in stubs})

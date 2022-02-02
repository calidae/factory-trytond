import factory
import pytest

import factory_trytond


class TestLazySearch():

    @pytest.mark.usefixtures('transaction')
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

        assert [stub.first for stub in stubs] == [foo1] * 10
        assert bar not in {stub.foo for stub in stubs}

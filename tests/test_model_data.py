import factory

import factory_trytond


class TestModelData():

    def test_model_data(self, pool):
        Lang = pool.get('ir.lang')
        Menu = pool.get('ir.ui.menu')

        class StubFactory(factory.StubFactory):
            english = factory_trytond.ModelData('ir', 'lang_en')
            admin = factory_trytond.ModelData('ir', 'menu_administration')

        stub = StubFactory.build()

        assert isinstance(stub.english, Lang)
        assert stub.english.name == 'English'

        assert isinstance(stub.admin, Menu)
        assert stub.admin.name == 'Administration'

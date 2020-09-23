import unittest

import factory

from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module
from trytond.tests.test_tryton import with_transaction

import factory_trytond


class ReferencesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @with_transaction()
    def test_many2one_subfactory_create(self):
        """Create a many2one relation with a subfactory"""
        Target = Pool().get('test.many2one_target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2one_target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2one'
            many2one = factory.SubFactory(TargetFactory)

        record = OriginFactory.create(many2one__value=42)

        self.assertCountEqual(Target.search([]), [record.many2one])
        self.assertEqual(record.many2one.value, 42)

    @with_transaction()
    def test_reference_subfactory_create(self):
        """Create a reference relation with a subfactory"""
        Target = Pool().get('test.reference.target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.reference.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.reference'
            reference = factory.SubFactory(TargetFactory)

        record = OriginFactory.create(reference__name='foo')

        self.assertCountEqual(Target.search([]), [record.reference])
        self.assertEqual(record.reference.name, 'foo')

    @with_transaction()
    def test_one2many_relatedfactory_create(self):
        """Create a one2many related object."""
        Target = Pool().get('test.one2many.target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.one2many.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.one2many'
            # Since `target` is a post-declaration, its value
            # will *not* be passed to the Origin constructor
            # but the `targets` one2many field will yield this
            # very record
            target = factory.RelatedFactory(
                TargetFactory,
                factory_related_name='origin',
            )
        record = OriginFactory.create(target__name='foo')

        self.assertTrue(record.targets)
        self.assertCountEqual(Target.search([]), record.targets)
        self.assertCountEqual(
            [target.name for target in record.targets],
            ['foo']
        )

    @with_transaction()
    def test_one2many_relatedfactorylist_create(self):
        """Create an object with one2many objects."""
        Target = Pool().get('test.one2many.target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.one2many.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.one2many'
            targets = factory.RelatedFactoryList(
                TargetFactory,
                factory_related_name='origin',
                size=1
            )
        record = OriginFactory.create(targets__name='foo')

        self.assertCountEqual(Target.search([]), record.targets)
        self.assertCountEqual(
            [target.name for target in record.targets],
            ['foo']
        )

    @with_transaction()
    def test_many2many_postdeclaration_create(self):
        """Create objects with many2many relations with a post-declaration"""
        Target = Pool().get('test.many2many.target')
        Origin = Pool().get('test.many2many')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many'

            @factory.post_generation
            def targets(obj, create, extracted, **kwargs):
                batch = (
                    TargetFactory.create_batch
                    if create
                    else TargetFactory.build_batch
                )
                obj.targets = extracted or batch(2, **kwargs)

        record = OriginFactory.create(targets__name='foo')

        self.assertCountEqual(Target.search([]), record.targets)
        self.assertCountEqual(Origin.search([]), [record])
        self.assertCountEqual(
            [t.name for t in record.targets],
            ['foo'] * 2
        )

    @with_transaction()
    def test_many2many_n_relatedfactory_create(self):
        """Create objects with many2many relations through
        multiple relatedfactory declarations for the relation model
        """
        Target = Pool().get('test.many2many.target')
        Origin = Pool().get('test.many2many')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many'

        class RelationFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many.relation'

            origin = factory.SubFactory(OriginFactory)
            target = factory.SubFactory(TargetFactory)

        class OriginWithTargetsFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2many'

            relation1 = factory.RelatedFactory(
                RelationFactory,
                factory_related_name='origin',
            )
            relation2 = factory.RelatedFactory(
                RelationFactory,
                factory_related_name='origin',
            )

        record = OriginFactory.create(
            # TODO: test relation target names
            # relation1__target__name='foo',
            # relation2__target__name='bar',
        )

        self.assertCountEqual(Target.search([]), record.targets)
        self.assertCountEqual(Origin.search([]), [record])

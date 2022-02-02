import factory

import factory_trytond


class TestReferences():

    def test_many2one_subfactory_create(self, pool):
        """Create a many2one relation with a subfactory"""
        Target = pool.get('test.many2one_target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2one_target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.many2one'
            many2one = factory.SubFactory(TargetFactory)

        record = OriginFactory.create(many2one__value=42)

        assert Target.search([]) == [record.many2one]
        assert record.many2one.value == 42

    def test_reference_subfactory_create(self, pool):
        """Create a reference relation with a subfactory"""
        Target = pool.get('test.reference.target')

        class TargetFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.reference.target'

        class OriginFactory(factory_trytond.TrytonFactory):
            class Meta:
                model = 'test.reference'
            reference = factory.SubFactory(TargetFactory)

        record = OriginFactory.create(reference__name='foo')

        assert Target.search([]) == [record.reference]
        assert record.reference.name == 'foo'

    def test_one2many_relatedfactory_create(self, pool):
        """Create a one2many related object."""
        Target = pool.get('test.one2many.target')

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

        assert record.targets
        assert Target.search([]) == list(record.targets)
        assert [target.name for target in record.targets] == ['foo']

    def test_one2many_relatedfactorylist_create(self, pool):
        """Create an object with one2many objects."""
        Target = pool.get('test.one2many.target')

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

        assert Target.search([]) == list(record.targets)
        assert [target.name for target in record.targets] == ['foo']

    def test_many2many_postdeclaration_create(self, pool):
        """Create objects with many2many relations with a post-declaration"""
        Target = pool.get('test.many2many.target')
        Origin = pool.get('test.many2many')

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

        assert Target.search([]) == list(record.targets)
        assert Origin.search([]) == [record]
        assert [t.name for t in record.targets] == ['foo'] * 2

    def test_many2many_n_relatedfactory_create(self, pool):
        """Create objects with many2many relations through
        multiple relatedfactory declarations for the relation model
        """
        Target = pool.get('test.many2many.target')
        Origin = pool.get('test.many2many')

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

        class OriginWithTargetsFactory(OriginFactory):
            relation1 = factory.RelatedFactory(
                RelationFactory,
                factory_related_name='origin',
            )
            relation2 = factory.RelatedFactory(
                RelationFactory,
                factory_related_name='origin',
            )

        record = OriginWithTargetsFactory.create(
            relation1__target__name='foo',
            relation2__target__name='bar',
        )

        assert Target.search([]) == sorted(record.targets)
        assert Origin.search([]) == [record]
        assert [t.name for t in record.targets] == ['bar', 'foo']

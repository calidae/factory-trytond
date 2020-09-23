# -*- coding: utf-8 -*-

import random
import factory
import factory.base

from trytond.pool import Pool
from trytond.transaction import Transaction


class TrytonOptions(factory.base.FactoryOptions):

    __active_database = False

    def get_model_class(self):
        if not self.__active_database and Transaction().database:
            self.__active_database = True
        if self.__active_database and isinstance(self.model, str):
            self.model = Pool().get(self.model)
        return super(TrytonOptions, self).get_model_class()

    def instantiate(self, step, args, kwargs):
        obj = super(TrytonOptions, self).instantiate(step, args, kwargs)
        self.factory.on_change(obj)
        if step.builder.strategy == factory.CREATE_STRATEGY:
            obj.save()
        return obj

    # This allows static tryton factories to be inherited
    def _get_counter_reference(self):
        if (
                self.model is not None
                and self.base_factory is not None
                and self.base_factory._meta.model is not None
                and (self.model == self.base_factory._meta.model)
        ):
            return self.base_factory._meta.counter_reference
        else:
            return self


class TrytonFactory(factory.Factory):
    _options_class = TrytonOptions

    @classmethod
    def create(cls, **kwargs):
        record = super(TrytonFactory, cls).create(**kwargs)
        record.save()
        return record

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        if create and results:
            obj.save()

    @classmethod
    def on_change(cls, record):
        pass


class LazySearch(factory.LazyAttribute):
    def __init__(self, model_name, function, limit=None, *args, **kwargs):
        def search(stub):
            Model = Pool().get(model_name)
            domain = function(stub)
            records = Model.search(domain, limit=limit)
            return random.choice(records) if records else None
        super(LazySearch, self).__init__(search, *args, **kwargs)


class ModelData(factory.LazyFunction):
    def __init__(self, module, fs_id, *args, **kwargs):
        def function():
            try:
                Data = Pool().get('ir.model.data')
                (data,) = Data.search([
                    ('module', '=', module),
                    ('fs_id', '=', fs_id),
                ])
                Model = Pool().get(data.model)
                return Model(data.db_id)
            except ValueError:
                return None
        super(ModelData, self).__init__(function, *args, **kwargs)

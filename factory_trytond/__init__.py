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
            self.model = Pool().get(self.model)
            self.__active_database = True
        return super(TrytonOptions, self).get_model_class()

    def instantiate(self, step, args, kwargs):
        obj = super(TrytonOptions, self).instantiate(step, args, kwargs)
        self.factory.on_change(obj)
        if step.builder.strategy == factory.CREATE_STRATEGY:
            obj.save()
        return obj


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


class LazySearch(factory.LazyFunction):
    def __init__(self, model_name, domain, limit=None, *args, **kwargs):
        def search():
            Model = Pool().get(model_name)
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

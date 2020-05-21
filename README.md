# Factory-trytond

Factory-trytond is a [factory_boy](https://factoryboy.readthedocs.io/en/latest/introduction.html) extension developed to work with [Tryton ERP](https://www.tryton.org/). We can create our own ERP's model factories to do some testing or to populate our databases with some sample data.

## How does it work?

Steps to use Factory-trytond:
1. Inherit the "base factory" class.
2. Define the "meta model" the factory "will construct".
3. Define the "default declarations" of the factory.
>Note that the meta model can be a *trytond pool model name*.

Here's a factory example with Tryton's model **User**:
```python
import factory
import factory_trytond

class UserFactory(factory_trytond.TrytonFactory):
    class Meta:
        model = 'res.user'

    name = factory.Faker('name')
    login = factory.Faker('user_name')

user = UserFactory.build()
user.save()  # it is a standard Tryton object as would be returned by Tryton's object pool
```

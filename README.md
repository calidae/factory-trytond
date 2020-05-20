# Factory-trytond

Factory-trytond is a [factory_boy](https://factoryboy.readthedocs.io/en/latest/introduction.html) extension developed to work with [Tryton ERP](https://www.tryton.org/). We can create our own ERP's model factories to do some testing or to populate our databases with some sample data.

## How does it work?

To use Factory-trytond your factory class only has to inherit the TrytonFactory:

    import factory_trytond

    class SaleFactory(factory_trytond.TrytonFactory):

Once we have inherited the class, we can start configuring our factory like we would do with factory_boy (e.g: define the class the factory is referring to, the fields the factory has to work with).
Here's an example with Tryton's model Sale:

    import factory
    import factory_trytond
    
    class SaleFactory(TrytonFactory):
        class Meta:
            model = 'sale.sale'

        company = factory.SubFactory(CompanyFactory)
        party = factory.SelfAttribute('franchise.company.party')
        franchise = factory.SubFactory(FranchiseFactory)
        currency = factory.SelfAttribute('company.currency')
        invoice_address = factory.LazyAttribute(
            lambda n: n.party.addresses[0]
        )


from crm.models.contacts import ContactMapper, Contact
from hdm.storage import SqlAlchemyStorage


def main():
    storage = SqlAlchemyStorage("postgresql://postgres:postgres@localhost:5432")
    mapper = ContactMapper(storage)
    storage.upgrade()
    contact = Contact(first_name="John", last_name="Doe", email="john@example.com")
    mapper.save(contact)
    print(repr(contact))
    contact.first_name = "Jane"
    contact.email = "jane@example.com"
    mapper.save(contact)
    print(repr(contact))


if __name__ == "__main__":
    main()

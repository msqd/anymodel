from typing import Optional

from hdm.entity import Entity
from hdm.mapper import Mapper


class Contact(Entity):
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    position: str = ""
    notes: str = ""


class ContactMapper(Mapper[Contact]):
    type = Contact
    name = "contacts"

    fields = ["first_name", "last_name", "email", "phone", "company", "position", "notes"]

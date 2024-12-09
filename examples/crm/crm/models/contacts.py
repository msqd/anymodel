from typing import Optional, List

from hdm.types.entity import Entity
from hdm.mapper import Mapper


class Contact(Entity):
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    position: str = ""
    notes: List[str] = ""


class ContactMapper(Mapper[Contact]):
    fields = {
        "first_name": ...,
        "last_name": ...,
        "email": ...,
        "phone": ...,
        "company": ...,
        "position": ...,
        "notes": ...,
    }

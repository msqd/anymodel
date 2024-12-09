HARP Data Mapper
================

``hdm`` is a data mapper built on top pydantic providing a flexible storage layer for extensible projects.

Write Plain Old Pydantic Objects, describe how the data are mapped to which storage (or storage combination) and let
``hdm`` do the rest.

Migrations are automatically handled by ``hdm``, you just have to describe the changes in your models and we'll diff
your database to apply the schema changes. As it sounds and is dangerous, a few safeguards are there to avoid data
loss due to a massive column drop.

Reqs
::::

We want to work with "popo" entities (here, plain old pydantic objects). We should be able to sync them back and forth
with nunderlying storages, but the storage implementation should not be tied to business objects.

Migrations should be automatic, yet not dangerous. Removed fields / tables should require an explicit confirmation from
the user, yet adding a field should be transparent.

We should be able to work with multiple storages at the same time, and even have a single entity mapped to multiple
storages, with a main/secondary logic (for example, an sql storage may be responsible for the key management, and store
the name, and a lucene index may store other things).

We should be able to manage lazy relations, and even lazy fields from secondary storages.


Journal
:::::::

7 dec 2024
----------

* mapper now manages simple one-to-many relations, some things are hardcoded, but it's a start. Relations are lazy
  loaded, and for now it's necessary to call the .load() method on the loaded entity to populate the related fields.

    -> we may need to autoload data on use? can be done later
    -> we need a way to chose a load strategy: eager, lazy ... not relevant for some storages, but sql will need it.

* we may need to combine MemoryStorage with MemoryTable from test utilities, as their purpose is the same.

-> the proof of concept in bin/sandbox.py should be refactored into tests, for the stable parts.

19 nov 2024
-----------

* reworking mapper vs storage api. Storage should probably not know about mapper, and mapper should be responsible for
  mapping. Wow.


18 nov 2024
-----------

* writing some tests
* reworking (in the test, wip) the mapper interface to it's more decoupled and able to work with more than one
  underlying storage.


TODO
::::

* do not delete tables or delete columns
* allow indexes to be created, searched by
* multimappers
* mapp to flat files that will write later to persistent storage?
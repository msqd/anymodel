HARP Data Mapper
================

``hdm`` is a data mapper built on top pydantic providing a flexible storage layer for extensible projects.

Write Plain Old Pydantic Objects, describe how the data are mapped to which storage (or storage combination) and let
``hdm`` do the rest.

Migrations are automatically handled by ``hdm``, you just have to describe the changes in your models and we'll diff
your database to apply the schema changes. As it sounds and is dangerous, a few safeguards are there to avoid data
loss due to a massive column drop.

Journal
:::::::

18 nov 2024
-----------

* writing some tests
* reworking (in the test, wip) the mapper interface to it's more decoupled and able to work with more than one underlying storage.


TODO
::::

* do not delete tables or delete columns
* allow indexes to be created, searched by
* multimappers
* mapp to flat files that will write later to persistent storage?
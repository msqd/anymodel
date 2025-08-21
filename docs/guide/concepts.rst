Core Concepts
=============

This guide explains the core concepts and components of AnyModel.

Collection
----------

A type-safe container for managing groups of entities. Collections track modifications and integrate with the mapper for persistence.

See :class:`anymodel.types.collections.Collection` for API details.

Entity
------

Base class for all domain objects. Extends Pydantic's BaseModel with state tracking capabilities for the data mapper pattern.

See :class:`anymodel.types.entity.Entity` for API details.

Field
-----

Field descriptor for entity properties. Re-exported from SQLModel, providing Pydantic field configuration plus SQL-specific features.

Mapper
------

Central component that handles persistence operations between entities and storage backends. Maintains identity mapping to prevent duplicates.

See :class:`anymodel.mapper.Mapper` for API details.

MemoryStorage
-------------

In-memory storage implementation useful for testing and temporary data. Stores entities in dictionaries without persistence.

See :class:`anymodel.storages.memory.MemoryStorage` for API details.

OneToManyRelation
-----------------

Represents a one-to-many relationship between entities. Supports lazy loading through mapper callbacks.

See :class:`anymodel.types.relations.OneToManyRelation` for API details.

Storage Backends
----------------

FileSystemStorage
~~~~~~~~~~~~~~~~~

Persists entities as JSON files on the filesystem. Useful for simple persistence without a database.

See :class:`anymodel.storages.filesystem.FileSystemStorage` for API details.

SqlAlchemyStorage
~~~~~~~~~~~~~~~~~

SQL database storage using SQLAlchemy. Supports automatic schema migrations and various database engines.

See :class:`anymodel.storages.sqlalchemy.SqlAlchemyStorage` for API details.

Architecture Patterns
---------------------

Identity Map
~~~~~~~~~~~~

The mapper maintains an identity map to ensure that only one instance of an entity with a given primary key exists in memory at any time. This prevents inconsistencies and reduces memory usage.

.. seealso::

    * `Identity map pattern (Martin Fowler) <https://martinfowler.com/eaaCatalog/identityMap.html>`_
    * `Identity map pattern (Wikipedia) <https://en.wikipedia.org/wiki/Identity_map_pattern>`_

Unit of Work
~~~~~~~~~~~~

Entities track their state (transient, dirty, clean) to optimize database operations. Only modified fields are updated during save operations.

.. seealso::

    * `Unit of Work pattern (Martin Fowler) <https://martinfowler.com/eaaCatalog/unitOfWork.html>`_
    * `Unit of Work pattern in Python (Cosmic Python) <https://www.cosmicpython.com/book/chapter_06_uow.html>`_

Data Mapper
~~~~~~~~~~~

Complete separation between domain objects (entities) and persistence logic (storage). Entities have no knowledge of how they are persisted.

.. seealso::

    * `Data Mapper pattern (Martin Fowler) <https://martinfowler.com/eaaCatalog/dataMapper.html>`_
    * `Data Mapper vs Active Record <https://culttt.com/2014/06/18/whats-difference-active-record-data-mapper/>`_

Lazy Loading
~~~~~~~~~~~~

Relations between entities are loaded on-demand to improve performance and reduce memory usage. Use ``mapper.load()`` to explicitly load relations when needed.

.. seealso::

    * `Lazy Load pattern (Martin Fowler) <https://martinfowler.com/eaaCatalog/lazyLoad.html>`_
    * `Lazy Loading best practices (Stack Overflow) <https://stackoverflow.com/questions/97197/what-is-lazy-loading>`_
AnyModel Documentation
======================

AnyModel is a modern data mapper library built on top of Pydantic that provides a flexible storage layer for Python applications. It allows mapping Plain Old Pydantic Objects to various storage backends with automatic migrations and lazy loading of relations.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guide/first-steps
   guide/concepts

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   reference/index

Features
--------

* **Pydantic-based entities** - Use familiar Pydantic models as your domain objects
* **Multiple storage backends** - SQL, filesystem, and in-memory storage options
* **Automatic migrations** - Schema changes are handled automatically
* **Lazy loading** - Relations are loaded on-demand for better performance
* **Identity mapping** - Prevents duplicate entity instances
* **Clean architecture** - Complete separation between domain and storage layers

Quick Start
-----------

.. code-block:: python

   from anymodel import Entity, Mapper, MemoryStorage
   from pydantic import Field

   class User(Entity):
       name: str
       email: str

   # Create storage and mapper
   storage = MemoryStorage()
   mapper = Mapper(User, storage)

   # Create and save entity
   user = User(name="Alice", email="alice@example.com")
   mapper.save(user)

   # Find entity
   found = mapper.find_one_by_pk(user.pk)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
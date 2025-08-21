First Steps
===========

This guide will walk you through the basics of using AnyModel to manage your domain entities with various storage backends.

Installation
------------

Install anymodel using your preferred package manager:

.. code-block:: bash

   pip install anymodel

Or with uv:

.. code-block:: bash

   uv add anymodel

Basic Concepts
--------------

AnyModel is built around several key concepts that work together to provide a clean data mapping solution:

* **Entity** - Your domain objects that extend Pydantic's BaseModel with state tracking
* **Mapper** - Handles persistence operations between entities and storage
* **Storage** - Backend implementations (memory, filesystem, SQL)
* **Collection** - Type-safe collections of entities
* **Relations** - Lazy-loaded relationships between entities

Creating Your First Entity
--------------------------

Entities are Pydantic models that inherit from ``Entity``. They automatically track their state (transient, dirty, or clean) and can be persisted to storage:

.. code-block:: python

   from anymodel import Entity, Field
   from datetime import datetime

   class Task(Entity):
       title: str
       description: str = ""
       completed: bool = False
       created_at: datetime = Field(default_factory=datetime.now)

The ``Field`` function is re-exported from SQLModel and provides all Pydantic field configuration options plus SQL-specific features.

Setting Up Storage and Mapper
------------------------------

AnyModel supports multiple storage backends. Let's start with the simplest one - in-memory storage:

.. code-block:: python

   from anymodel import Mapper, MemoryStorage

   # Create storage instance
   storage = MemoryStorage()

   # Create mapper for your entity
   task_mapper = Mapper(Task, storage)

The mapper handles all CRUD operations and maintains an identity map to prevent duplicate instances.

Basic Operations
----------------

Creating and Saving Entities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a new task
   task = Task(
       title="Learn HDM",
       description="Read the documentation and try examples"
   )

   # Save to storage
   task_mapper.save(task)
   print(f"Task saved with ID: {task.pk}")

Finding Entities
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find by primary key
   task = task_mapper.find_one_by_pk("task-id-here")

   # Find all tasks
   all_tasks = task_mapper.find()

   # Find with filters (storage-specific)
   completed_tasks = task_mapper.find({"completed": True})

Updating Entities
~~~~~~~~~~~~~~~~~

Entities automatically track changes. Simply modify the entity and save:

.. code-block:: python

   task = task_mapper.find_one_by_pk(task_id)
   task.completed = True
   task_mapper.save(task)  # Only updates changed fields

Deleting Entities
~~~~~~~~~~~~~~~~~

.. code-block:: python

   task = task_mapper.find_one_by_pk(task_id)
   task_mapper.delete(task)

Working with Collections
------------------------

Collections provide a type-safe way to work with groups of entities:

.. code-block:: python

   from anymodel import Collection

   class Project(Entity):
       name: str
       tasks: Collection[Task] = Collection()

   project = Project(name="My Project")
   project.tasks.append(Task(title="First task"))
   project.tasks.append(Task(title="Second task"))

   # Collections are iterable
   for task in project.tasks:
       print(task.title)

Entity Relations
----------------

AnyModel supports lazy-loaded relations between entities:

.. code-block:: python

   from anymodel import OneToManyRelation

   class Author(Entity):
       name: str
       posts: OneToManyRelation["Post"] = OneToManyRelation()

   class Post(Entity):
       title: str
       content: str
       author_id: str

   # Relations are loaded on demand
   author = author_mapper.find_one_by_pk(author_id)
   author_mapper.load(author, "posts")  # Explicitly load relation
   
   for post in author.posts:
       print(post.title)

Using Different Storage Backends
---------------------------------

Filesystem Storage
~~~~~~~~~~~~~~~~~~

Store entities as JSON files:

.. code-block:: python

   from anymodel.storages.filesystem import FileSystemStorage

   storage = FileSystemStorage(directory="./data")
   mapper = Mapper(Task, storage)

SQL Storage
~~~~~~~~~~~

Use SQLAlchemy for relational databases:

.. code-block:: python

   from anymodel.storages.sqlalchemy import SqlAlchemyStorage
   from sqlalchemy import create_engine

   engine = create_engine("sqlite:///tasks.db")
   storage = SqlAlchemyStorage(engine)
   mapper = Mapper(Task, storage)

Next Steps
----------

* Read the :doc:`concepts` guide for deeper understanding
* Explore the API reference for :doc:`../reference/anymodel.types` and :doc:`../reference/anymodel.storages`
* Check out the examples in the repository for real-world usage patterns
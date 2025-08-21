# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AnyModel is a modern data mapper library built on top of Pydantic that provides a flexible storage layer for Python applications. It allows mapping Plain Old Pydantic Objects to various storage backends (SQL, filesystem, memory) with automatic migrations and lazy loading of relations.

## Development Commands

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_mapper.py

# Run specific test
uv run pytest tests/test_mapper.py::test_basics

# Run tests with verbose output
uv run pytest -v
```

### Code Quality
```bash
# Run linter
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package>

# Add development dependency
uv add --group dev <package>
```

## Architecture

### Core Components

**Entity System** (`anymodel/types/entity.py`)
- Base class `Entity` extends Pydantic's BaseModel
- Includes `__state__` property for tracking mapping state (transient/dirty/clean)
- Entities track modifications through Pydantic's field tracking

**Mapper** (`anymodel/mapper.py`)
- Generic mapper class that handles entity-to-storage mapping
- Manages primary keys, relations, and identity mapping
- Key methods: `save()`, `find_one_by_pk()`, `find()`, `load()`
- Supports caching via IdentityMap

**Storage Layer** (`anymodel/storages/`)
- Abstract `Storage` base class defines interface
- Implementations: `MemoryStorage`, `SqlAlchemyStorage`, `FilesystemStorage`
- Storage is decoupled from business logic - knows nothing about entities

**Relations** (`anymodel/types/relations.py`)
- Support for lazy-loaded relations
- Currently implements `OneToManyRelation`
- Relations are resolved through mapper callbacks

### Key Design Patterns

1. **Identity Map Pattern**: Prevents duplicate entity instances via `IdentityMap` class
   - [Martin Fowler's Identity Map](https://martinfowler.com/eaaCatalog/identityMap.html)
   - [Identity Map Pattern Explained](https://www.sourcecodeexamples.net/2018/04/identity-map-pattern.html)

2. **Unit of Work**: Entities track their state (clean/dirty/transient) for efficient updates
   - [Martin Fowler's Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html)
   - [Unit of Work Pattern in Python](https://www.cosmicpython.com/book/chapter_06_uow.html)

3. **Data Mapper**: Complete separation between domain objects and storage layer
   - [Martin Fowler's Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html)
   - [Data Mapper vs Active Record](https://culttt.com/2014/06/18/whats-difference-active-record-data-mapper/)

4. **Lazy Loading**: Relations are loaded on-demand via callbacks
   - [Martin Fowler's Lazy Load](https://martinfowler.com/eaaCatalog/lazyLoad.html)
   - [Lazy Loading Best Practices](https://stackoverflow.com/questions/97197/what-is-lazy-loading)

## Testing Requirements

Before writing any new code:
1. Analyze existing test coverage with `uv run pytest --cov=anymodel`
2. Ensure existing functionality has 100% unit test coverage
3. Write tests for new features before implementation
4. All tests must pass before considering task complete

## Code Style Guidelines

- Line length: 120 characters (configured in pyproject.toml)
- Use type hints for all function signatures
- Write concise docstrings for all public methods and classes
- Follow existing patterns in the codebase for consistency
- No trailing comments or unnecessary code comments

## Current Development Focus

Based on the journal in README.rst:
- Mapper manages simple one-to-many relations (requires `.load()` call)
- Multi-storage support is being developed
- Automatic migrations with safeguards against data loss
- Need to prevent accidental table/column deletion
- Index creation and search functionality planned
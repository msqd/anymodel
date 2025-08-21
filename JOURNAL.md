# Journal

## 7 dec 2024

* mapper now manages simple one-to-many relations, some things are hardcoded, but it's a start. Relations are lazy
  loaded, and for now it's necessary to call the .load() method on the loaded entity to populate the related fields.

  -> we may need to autoload data on use? can be done later
  -> we need a way to chose a load strategy: eager, lazy ... not relevant for some storages, but sql will need it.

* we may need to combine MemoryStorage with MemoryTable from test utilities, as their purpose is the same.

-> the proof of concept in bin/sandbox.py should be refactored into tests, for the stable parts.

## 19 nov 2024

* reworking mapper vs storage api. Storage should probably not know about mapper, and mapper should be responsible for
  mapping. Wow.


## 18 nov 2024

* writing some tests
* reworking (in the test, wip) the mapper interface to it's more decoupled and able to work with more than one
  underlying storage.


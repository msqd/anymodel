#!/usr/bin/env python
"""Generate Sphinx reference documentation for AnyModel modules."""

import ast
import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import List, Set, Tuple


def get_module_members(module_name: str) -> List[Tuple[str, str]]:
    """Get public members of a module with their types."""
    members = []
    try:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if not name.startswith("_"):
                if inspect.isclass(obj):
                    members.append((name, "class"))
                elif inspect.isfunction(obj):
                    members.append((name, "function"))
                elif inspect.ismodule(obj) and obj.__name__.startswith(module_name):
                    # Skip submodules, they'll be handled separately
                    pass
                else:
                    # Could be a constant or other type
                    members.append((name, "data"))
    except ImportError:
        pass
    return members


def find_all_modules(package_name: str, package_path: Path) -> List[str]:
    """Recursively find all public Python modules in a package."""
    modules = []

    # Add the parent package to path temporarily
    sys.path.insert(0, str(package_path.parent))

    try:
        # Import the main package
        package = importlib.import_module(package_name)

        # Walk through all submodules
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package.__path__, prefix=package.__name__ + ".", onerror=lambda x: None
        ):
            # Skip private modules (those with any component starting with _)
            parts = modname.split(".")
            if any(part.startswith("_") for part in parts):
                continue
            modules.append(modname)

    except ImportError as e:
        print(f"Warning: Could not import {package_name}: {e}")
    finally:
        sys.path.pop(0)

    # Sort modules by depth and name for better organization
    modules.sort(key=lambda x: (x.count("."), x))
    return modules


def parse_module_file(file_path: Path) -> Set[str]:
    """Parse a Python file to find defined classes and functions."""
    classes = set()
    functions = set()

    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                classes.add(node.name)
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                functions.add(node.name)

    except (SyntaxError, FileNotFoundError):
        pass

    return classes | functions


def generate_module_rst(module_path: str, output_path: Path, package_name: str, seen_objects: Set[str]) -> None:
    """Generate RST file for a module.

    Args:
        module_path: The module path (e.g., 'anymodel.storages.base')
        output_path: The output directory for RST files
        package_name: The main package name
        seen_objects: Set of already documented objects (to avoid duplicates)
    """
    output_file = output_path / f"{module_path}.rst"

    # Create a nice title
    title = f"{module_path}"
    underline = "=" * len(title)

    # Get module members to check what's in the module
    members = get_module_members(module_path)

    # Separate defined vs imported members
    defined_classes = []
    imported_classes = []
    defined_functions = []
    imported_functions = []
    defined_classes_full_paths = {}  # Map class name to its actual module path
    defined_functions_full_paths = {}  # Map function name to its actual module path

    try:
        module = importlib.import_module(module_path)
        for name, type_ in members:
            if type_ == "class":
                cls = getattr(module, name, None)
                if cls and hasattr(cls, "__module__"):
                    actual_module = cls.__module__
                    full_path = f"{actual_module}.{name}"
                    if actual_module == module_path:
                        defined_classes.append(name)
                        defined_classes_full_paths[name] = full_path
                    else:
                        imported_classes.append(name)
            elif type_ == "function":
                func = getattr(module, name, None)
                if func and hasattr(func, "__module__"):
                    actual_module = func.__module__
                    full_path = f"{actual_module}.{name}"
                    if actual_module == module_path:
                        defined_functions.append(name)
                        defined_functions_full_paths[name] = full_path
                    else:
                        imported_functions.append(name)
    except Exception:
        # Fallback if module can't be imported
        defined_classes = [name for name, type_ in members if type_ == "class"]
        defined_functions = [name for name, type_ in members if type_ == "function"]
        # Use current module path for full paths in fallback
        for name in defined_classes:
            defined_classes_full_paths[name] = f"{module_path}.{name}"
        for name in defined_functions:
            defined_functions_full_paths[name] = f"{module_path}.{name}"

    # Start with module title
    content = f"""{title}
{underline}

"""

    # For the main anymodel module, only show the module docstring and imported members
    if module_path == "anymodel":
        # Only show module docstring - members are documented in their definition modules
        content += f""".. automodule:: {module_path}
   :no-members:

"""
        # Show what's available at package level
        if imported_classes or imported_functions:
            content += "\nAvailable at package level:\n\n"
            all_imports = imported_classes + imported_functions
            for name in sorted(all_imports):
                content += f"* :obj:`~{module_path}.{name}`\n"
            content += "\n"
    # If this is a package __init__ module with re-exports, list them
    elif module_path.endswith((".storages", ".types", ".utilities")) and (imported_classes or imported_functions):
        # Just show the module docstring with no members
        content += f""".. automodule:: {module_path}
   :no-members:

"""
        # Show what's available at package level
        if imported_classes or imported_functions:
            content += "\nAvailable at package level:\n\n"
            all_imports = imported_classes + imported_functions
            for name in sorted(all_imports):
                content += f"* :obj:`~{module_path}.{name}`\n"
            content += "\n"
    elif not defined_classes and not defined_functions:
        # Module with no local definitions
        content += f""".. automodule:: {module_path}
   :members:
   :undoc-members:
   :show-inheritance:

"""
    else:
        # Module with local definitions - just show docstring, members are documented below
        content += f""".. automodule:: {module_path}
   :no-members:

"""

    # Add detailed documentation for locally defined classes only
    if defined_classes:
        content += "\nClasses\n-------\n\n"
        for class_name in sorted(defined_classes):
            # Get the actual full path of this class
            actual_full_path = defined_classes_full_paths.get(class_name, f"{module_path}.{class_name}")

            # Check if this object has been documented before using its actual path
            if actual_full_path in seen_objects:
                # Add with :no-index: to avoid duplicate warnings
                content += f""".. autoclass:: {module_path}.{class_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
   :no-index:

"""
            else:
                # First time documenting this object
                seen_objects.add(actual_full_path)
                content += f""".. autoclass:: {module_path}.{class_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

"""

    # Add detailed documentation for locally defined functions only
    if defined_functions:
        content += "\nFunctions\n---------\n\n"
        for func_name in sorted(defined_functions):
            # Get the actual full path of this function
            actual_full_path = defined_functions_full_paths.get(func_name, f"{module_path}.{func_name}")

            # Check if this function has been documented before using its actual path
            if actual_full_path in seen_objects:
                # Add with :no-index: to avoid duplicate warnings
                content += f""".. autofunction:: {module_path}.{func_name}
   :no-index:

"""
            else:
                # First time documenting this function
                seen_objects.add(actual_full_path)
                content += f""".. autofunction:: {module_path}.{func_name}

"""

    # Ensure parent directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(content)
    print(f"Generated {output_file}")


def generate_index_rst(package_name: str, modules: List[str], output_path: Path) -> None:
    """Generate an index.rst file for the API reference."""
    index_file = output_path / "index.rst"

    content = f"""API Reference
=============

This is the complete API reference for {package_name}.

.. toctree::
   :maxdepth: 2
   :caption: Modules

"""

    # Group modules by top-level package
    module_groups = {}
    for module in modules:
        parts = module.split(".")
        if len(parts) > 1:
            group = parts[1]  # e.g., 'types', 'storages', etc.
            # Skip private groups
            if group.startswith("_"):
                continue
            if group not in module_groups:
                module_groups[group] = []
            module_groups[group].append(module)

    # Add main package
    content += f"   {package_name}\n"

    # Add grouped modules
    for group in sorted(module_groups.keys()):
        # Format group name for display
        display_name = group.replace("_", " ").title()
        content += f"\n{display_name}\n{'-' * len(display_name)}\n\n.. toctree::\n   :maxdepth: 1\n\n"
        for module in sorted(module_groups[group]):
            content += f"   {module}\n"

    index_file.write_text(content)
    print(f"Generated {index_file}")


def sort_modules_hierarchically(modules: List[str]) -> List[str]:
    """Sort modules in hierarchical order (parent before child).

    This ensures that parent modules are processed before their children,
    so we can track which objects have already been documented.
    """
    # Create a list of tuples with (depth, module_name)
    modules_with_depth = []
    for module in modules:
        depth = module.count(".")
        modules_with_depth.append((depth, module))

    # Sort by depth first, then by name
    modules_with_depth.sort(key=lambda x: (x[0], x[1]))

    # Return just the module names
    return [module for _, module in modules_with_depth]


def main():
    """Generate reference documentation for all AnyModel modules."""
    # Get the project root (parent of bin directory)
    project_root = Path(__file__).parent.parent
    package_name = "anymodel"
    package_path = project_root / package_name
    docs_reference = project_root / "docs" / "reference"

    if not package_path.exists():
        print(f"Error: Package directory '{package_path}' not found!")
        return

    # Ensure reference directory exists
    docs_reference.mkdir(parents=True, exist_ok=True)

    # Find all modules in the package
    print(f"Discovering modules in {package_name}...")
    modules = find_all_modules(package_name, package_path)

    if not modules:
        print("No modules found!")
        return

    # Sort modules hierarchically (parent before child)
    modules = sort_modules_hierarchically(modules)

    print(f"Found {len(modules) + 1} modules:")
    print(f"  - {package_name}")
    for module in modules:
        print(f"  - {module}")

    # Track which objects have been documented to avoid duplicates
    seen_objects: Set[str] = set()

    # Generate documentation for main package
    print("\nGenerating documentation...")
    generate_module_rst(package_name, docs_reference, package_name, seen_objects)

    # Generate documentation for each module (in hierarchical order)
    for module in modules:
        generate_module_rst(module, docs_reference, package_name, seen_objects)

    # Generate index file
    generate_index_rst(package_name, modules, docs_reference)

    print(f"\nReference documentation generated in {docs_reference}")
    print("Run 'make docs' to build the full documentation")


if __name__ == "__main__":
    main()

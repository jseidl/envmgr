import sys
import inspect
import importlib

from envmgr.constants import COMPONENT_BACKEND, COMPONENT_ENCRYPTION


def load_component(component_type, component_name):

    import_path = f"{__package__}.{component_type}.{component_name}"

    module = importlib.import_module(import_path)
    class_members = inspect.getmembers(sys.modules[import_path], inspect.isclass)

    class_name = None

    for name, obj in class_members:
        if name.lower() == component_name.lower():
            class_name = name
            break

    if not class_name:
        raise ImportError(f"{component_type} '{component_name}' doesn't exists.")

    return getattr(module, class_name)


def load_backend(name):

    return load_component(COMPONENT_BACKEND, name)


def load_encryption(name):

    return load_component(COMPONENT_ENCRYPTION, name)

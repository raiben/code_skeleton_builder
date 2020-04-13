from typing import TypeVar, Type, Any


class ObjectFactory(object):
    interface_implementation_map = {}

    @classmethod
    def add_implementation(cls, source_interface, target_implementation):
        cls.interface_implementation_map[source_interface] = target_implementation

    T = TypeVar('T')

    @classmethod
    def build_instance(cls, source_interface, *args, **kwargs):
        # type: (Type[T], Any, Any) -> T
        return cls.interface_implementation_map[source_interface](*args, **kwargs)

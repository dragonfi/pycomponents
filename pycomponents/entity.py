class Entity(object):
    next_id = 0

    def __init__(self, *components):
        self.id = Entity.next_id
        Entity.next_id += 1

        self.components = set()
        for component in components:
            self.add(component)

    def add(self, component):
        if type(component) == type:
            component = component()
        setattr(self, component.__class__.__name__, component)
        self.components.add(component.__class__)

    def remove(self, component_class):
        self.components.remove(component_class)

    def has(self, component_class):
        return component_class in self.components


def Component(name, **attributes):
    """Returns a new component"""
    attributes['__init__'] = Component__init__
    return type(name, (), dict(**attributes))


def Component__init__(self, **attributes):
        if not set(attributes).issubset(set(self.__class__.__dict__)):
            raise AttributeError("No such attribute in class")
        self.__dict__.update(attributes)


def system(*components, **attributes):
    """A decorator to create a system definition."""
    def system_inner(fn):
        fn.components = tuple(components)
        fn.__dict__.update(attributes)
        def fn__init__(**inner_attributes):
            if not set(inner_attributes).issubset(set(attributes)):
                raise AttributeError("No such attribute on function")
            fn.__dict__.update(inner_attributes)
            return fn
        return fn__init__
    return system_inner

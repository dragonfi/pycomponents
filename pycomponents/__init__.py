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

    def has(self, *component_classes):
        return set(component_classes).issubset(self.components)


def Component(name, **attributes):
    """Returns a new component"""
    attributes['__init__'] = _Component__init__
    return type(name, (), dict(**attributes))


def _Component__init__(self, **attributes):
        if not set(attributes).issubset(set(self.__class__.__dict__)):
            raise AttributeError("No such attribute in class")
        self.__dict__.update(attributes)


def System(components, **attributes):
    """A decorator to create a system definition."""
    def system_inner(fn):
        fn.components = tuple(components)
        fn.__dict__.update(attributes)

        def fn__init__(**inner_attributes):
            if not set(inner_attributes).issubset(set(attributes)):
                raise AttributeError("No such attribute on function")
            fn.__dict__.update(inner_attributes)
            fn__init__.__dict__.update(fn.__dict__)
            return fn
        return fn__init__
    return system_inner


class World(object):
    def __init__(self):
        self._entities = []
        self._systems = []

    def add(self, *objs):
        for obj in objs:
            if isinstance(obj, Entity):
                self.add_entity(obj)
            elif callable(obj):
                self.add_system(obj)

    def add_entity(self, entity):
        self._entities.append(entity)

    def add_system(self, system):
        self._systems.append(system)

    def entities(self, has=None):
        if not has:
            return list(self._entities)
        else:
            components = has
            return list(filter(lambda e: e.has(*components), self._entities))

    def systems(self):
        return list(self._systems)

    def remove(self, obj):
        if isinstance(obj, Entity):
            self.remove_entity(obj)
        elif callable(obj):
            self.remove_system(obj)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    def remove_system(self, system):
        self._systems.remove(system)

    def update(self, dt):
        self.dt = dt
        for system in self.systems():
            for entity in self.entities(has=system.components):
                system(entity, self)

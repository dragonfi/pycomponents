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
        setattr(self, component.name, component)
        self.components.add(component.__class__)

    def remove(self, component_class):
        self.components.remove(component_class)

    def has(self, *component_classes):
        return set(component_classes).issubset(self.components)


class _UpdateAttributesOnInit(object):
    def __init__(self, **attributes):
        if not set(attributes).issubset(set(self.__class__.__dict__)):
            raise AttributeError("No such attribute in class")
        self.__dict__.update(attributes)


class Component(_UpdateAttributesOnInit):
    name = None

    def __init__(self, **attributes):
        super().__init__(**attributes)
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        if not self.name.isidentifier():
            msg = "component name must be a valid identifier: '{}'".format(
                self.name)
            raise ValueError(msg)


class System(_UpdateAttributesOnInit):
    pass


class World(object):
    def __init__(self):
        self._entities = []
        self._systems = []

    def add(self, *objs):
        for obj in objs:
            if isinstance(obj, Entity):
                self.add_entity(obj)
            elif isinstance(obj, System):
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
        elif isinstance(obj, System):
            self.remove_system(obj)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    def remove_system(self, system):
        self._systems.remove(system)

    def update(self, dt):
        self.dt = dt
        for system in self.systems():
            for entity in self.entities(has=system.components):
                system.update(entity, self)

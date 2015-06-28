class Entity(object):
    next_id = 0

    def __init__(self):
        self.id = Entity.next_id
        self.components = set()
        Entity.next_id += 1

    def add(self, component):
        component.add_to(self)

    def remove(self, component_class):
        self.components.remove(component_class)

    def has(self, component_class):
        return component_class in self.components


class Component(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def add_to(self, entity):
        entity.components.add(self.__class__)
        self.init(entity, *self.args, **self.kwargs)

    def init(self, entity):
        raise NotImplementedError


class World(object):
    pass

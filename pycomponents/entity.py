class Entity(object):
    next_id = 0

    def __init__(self, *args):
        self.id = Entity.next_id
        Entity.next_id += 1

        self.components = set()
        for component in args:
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


def Component(name, **kwargs):
    kwargs['__init__'] = Component__init__
    return type(name, (), dict(**kwargs))


def Component__init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr not in self.__class__.__dict__:
                raise AttributeError("No such attribute in class")
            setattr(self, attr, value)



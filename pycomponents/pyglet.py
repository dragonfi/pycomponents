import pyglet

from pycomponents.core import System, World


class RenderingSystem(System):
    def update(self, entity, world):
        pass

    def draw_all(self, entities, world):
        raise NotImplementedError


class PygletGame(pyglet.window.Window):
    def __init__(self, world=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if world is None:
            world = World()
        self.world = world

    def add(self, *objs):
        self.world.add(*objs)

    def remove(self, obj):
        self.world.remove(obj)

    def on_draw(self):
        self.clear()
        for system in self.world.systems(RenderingSystem):
            entities = self.world.entities(has=system.components)
            system.draw_all(entities, self.world)

    def run(self):
        pyglet.clock.schedule_interval(self.world.update, 0.01)
        pyglet.app.run()

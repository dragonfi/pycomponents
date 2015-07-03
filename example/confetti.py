#!/usr/bin/env python3

import pyglet
import itertools
import random

import os
import sys
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
from pycomponents import Component, Entity, System, World


class Point(Component):
    name = "point"
    x = 0
    y = 0

class Velocity(Component):
    x = 0
    y = 0

class Color(Component):
    name = "color"
    r = 255
    g = 255
    b = 255
    a = 255

class Integrator(System):
    components = [Point, Velocity]
    def update(self, entity, world):
        entity.point.x += entity.velocity.x * world.dt
        entity.point.y += entity.velocity.y * world.dt


class BorderBouncer(System):
    components = [Point, Velocity]
    width = 0
    height = 0
    border = 10
    def update(self, entity, world):
        if not self.border < entity.point.x < self.width - self.border:
            entity.velocity.x *= -1
        if not self.border < entity.point.y < self.height - self.border:
            entity.velocity.y *= -1



class RandomMover(System):
    components = [Point]

    def update(self, entity, world):
        entity.point.x += random.random() - 0.5
        entity.point.y += random.random() - 0.5


class RandomImpulse(System):
    components = [Velocity]
    def update(self, entity, world):
        entity.velocity.x += (random.random() - 0.5) * world.dt * 100
        entity.velocity.y += (random.random() - 0.5) * world.dt * 100



class RenderingSystem(System):
    def update(self, entity, world):
        pass
    def draw_all(self, entities, world):
        raise NotImplementedError

class FPSDisplay(RenderingSystem):
    components = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fps_display = pyglet.clock.ClockDisplay()
    def draw_all(self, entities, world):
        self.fps_display.draw()


class DebugDraw(RenderingSystem):
    components = [Point, Color]

    def draw_all(self, entities, world):
        pyglet.gl.glPointSize(5)
        v2f = [(e.point.x, e.point.y) for e in entities]
        v2f = tuple(itertools.chain.from_iterable(v2f))
        c4B = [(e.color.r, e.color.g, e.color.b, e.color.a) for e in entities]
        c4B = tuple(itertools.chain.from_iterable(c4B))
        points = pyglet.graphics.vertex_list(
            len(entities), ('v2f', v2f), ('c4B', c4B))
        points.draw(pyglet.gl.GL_POINTS)


class KeyboardControl(System):
    components = [Point]

    def update(self, entity, world):
        pass


class PygletGame(pyglet.window.Window):
    def __init__(self, world=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if world is None: world = World()
        self.world = world

    def add(self, *objs):
        self.world.add(*objs)

    def on_draw(self):
        self.clear()
        for system in self.world.systems(RenderingSystem):
            entities = self.world.entities(has=system.components)
            system.draw_all(entities, self.world)

    def on_key_press(self, sym, mod):
        if sym == pyglet.window.key.A:
            print("A is pressed")
        super().on_key_press(sym, mod)

    def run(self):
        pyglet.clock.schedule_interval(self.world.update, 0.01)
        pyglet.app.run()


class Game(PygletGame):
    pass


game = PygletGame()
game.add(
    FPSDisplay(), DebugDraw(),
    RandomImpulse(), Integrator(),
    BorderBouncer(width=game.width, height=game.height))

border = 100
for i in range(border, game.width - border, 10):
    for j in range(border, game.height - border, 10):
        game.add(Entity(
            Point(x=i, y=j), Velocity(x=0, y=0),
            Color(r=i+j, g=i-j, b=i*j, a=255)))

#game.add(Entity(Point(x=10, y=10)), Entity(Point(x=100, y=100)))
game.run()

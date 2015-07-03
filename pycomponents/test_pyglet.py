import unittest

import sys
from unittest import mock
sys.modules['pyglet'] = mock.Mock()


class MockWindow(object):
    clear = mock.Mock()

import pyglet
pyglet.window.Window = MockWindow

from pycomponents.core import World, Entity
from pycomponents.pyglet import PygletGame, RenderingSystem


class TestPygletWrapper(unittest.TestCase):
    def test_rendering_system_has_a_callable_update_method(self):
        class ExampleDrawer(RenderingSystem):
            pass

        ed = ExampleDrawer()
        ed.update(None, None)

    def test_rendering_system_must_have_a_draw_all_method(self):
        class ExampleDrawer(RenderingSystem):
            pass

        ed = ExampleDrawer()
        with self.assertRaises(NotImplementedError):
            ed.draw_all(None, None)

    def test_pyglet_game_wraps_world_properly(self):
        world = World()
        entity = Entity()

        game = PygletGame(world)
        self.assertEqual(game.world, world)

        game.add(entity)
        self.assertIn(entity, world.entities())

        game.remove(entity)
        self.assertNotIn(entity, world.entities())

    def test_pyglet_game_on_draw_calls_rendering_systems(self):
        game = PygletGame()

        drawer = mock.Mock(RenderingSystem, components=[])
        game.add(drawer)

        self.assertFalse(drawer.draw_all.called)

        game.on_draw()
        self.assertTrue(drawer.draw_all.called)

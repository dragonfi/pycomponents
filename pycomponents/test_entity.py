import unittest
import typesafety

from .entity import Entity, Component, World

Component1 = Component(attribute=True, counter=0)
Component2 = Component(attribute=True)

class Component1(Component):
    def init(self, entity):
        entity.component1_attribute = True
        entity.component1_counter = 0


class Component2(Component):
    def init(self, entity):
        entity.c2_attribute = True


class BaseTestCase(unittest.TestCase):
    def assertHasAttr(self, obj, attr):
        if not hasattr(obj, attr):
            msg = "{} has no attribute '{}'".format(obj, attr)
            raise AssertionError(msg)


class TestEntity(BaseTestCase):
    def test_entity_has_an_id(self):
        entity = Entity()
        self.assertHasAttr(entity, 'id')

    def test_different_entities_has_differing_ids(self):
        entity1 = Entity()
        entity2 = Entity()
        self.assertNotEquals(entity1.id, entity2.id)

    def test_components_can_be_removed(self):
        entity = Entity()
        entity.add(Component1())
        self.assertTrue(entity.has(Component1))
        entity.remove(Component1)
        self.assertFalse(entity.has(Component1))


class TestComponent(BaseTestCase):
    def test_components_can_be_added_to_an_entity(self):
        entity = Entity()
        entity.add(Component1())
        self.assertEquals(entity.has(Component1), True)

    def test_components_add_their_attributes_to_entity(self):
        entity = Entity()
        entity.add(Component1())
        self.assertHasAttr(entity, 'component1_attribute')

    def test_component_add_to_can_also_add_the_component(self):
        entity = Entity()
        component1 = Component1()
        component1.add_to(entity)
        self.assertEquals(entity.has(Component1), True)
        self.assertHasAttr(entity, 'component1_attribute')


class World(BaseTestCase):
    def test_world_can_be_instantiated(self):
        world = World()

    def xtest_entities_can_be_added_to_world(self):
        world = World()
        entity = Entity(Component1, Component2)
        self.assertIn(entity, world.entities)

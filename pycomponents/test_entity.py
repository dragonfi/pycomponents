import unittest
import typesafety

from .entity import Entity, Component, system

Position = Component('position', x=0, y=0)
Velocity = Component('velocity', x=0, y=0)


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


class TestEntityComponent(BaseTestCase):
    def test_entity_can_be_instantiated_with_multiple_components(self):
        entity = Entity(Position, Velocity)

        self.assertHasAttr(entity, 'position')
        self.assertHasAttr(entity, 'velocity')
        self.assertTrue(entity.has(Position))
        self.assertTrue(entity.has(Velocity))

    def test_components_can_be_added_after_intantiation(self):
        entity = Entity()
        self.assertFalse(entity.has(Position))

        entity.add(Position)
        self.assertTrue(entity.has(Position))

    def test_components_can_be_removed(self):
        entity = Entity()
        entity.add(Position)
        self.assertTrue(entity.has(Position))

        entity.remove(Position)
        self.assertFalse(entity.has(Position))


class TestComponent(BaseTestCase):
    def test_can_only_be_instantiated_with_predefined_attributes(self):
        with self.assertRaises(AttributeError):
            p = Position(x=10, y=12, z=10)

    def test_component_can_have_properties(self):
        def diff(self):
            return abs(self.high - self.low)
        Interval = Component('interval', low=0, high=0, diff=property(diff))
        self.assertTrue(Interval(low=10, high=15).diff, 5)


@system(Position, Velocity, dampening=0.9)
def physics(entity, world):
    entity.position.x += entity.velocity.x * world.dt
    entity.position.y += entity.velocity.y * world.dt

    entity.velocity.x *= physics.dampening
    entity.velocity.y *= physics.dampening


class TestSystem(BaseTestCase):
    def test_system_can_be_created(self):
        p = physics()
        self.assertEquals(p.components, (Position, Velocity))
        self.assertEquals(p.dampening, 0.9)

    def test_system_can_have_variables(self):
        p = physics(dampening=0.8)
        self.assertEquals(p.dampening, 0.8)

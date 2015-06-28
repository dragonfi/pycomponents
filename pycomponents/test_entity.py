import unittest
import typesafety

from . import Entity, Component, System, World

Position = Component('position', x=0, y=0)
Velocity = Component('velocity', x=0, y=0)


@System([Position, Velocity], dampening=0.9)
def physics(entity, world):
    entity.position.x += entity.velocity.x * world.dt
    entity.position.y += entity.velocity.y * world.dt

    factor = max(0, (1 - physics.dampening))
    entity.velocity.x *= factor
    entity.velocity.y *= factor


class BaseTestCase(unittest.TestCase):
    def assertHasAttr(self, obj, attr):
        if not hasattr(obj, attr):
            msg = "{} has no attribute '{}'".format(obj, attr)
            raise AssertionError(msg)

    def assertLen(self, seq, length):
        if not len(seq) == length:
            msg = "{} should have length of '{}'".format(seq, length)
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

    def test_has_tests_if_entity_has_all_components(self):
        entity = Entity(Position, Velocity)
        self.assertTrue(entity.has(Position, Velocity))

        entity.remove(Velocity)
        self.assertFalse(entity.has(Position, Velocity))


class TestComponent(BaseTestCase):
    def test_can_only_be_instantiated_with_predefined_attributes(self):
        with self.assertRaises(AttributeError):
            p = Position(x=10, y=12, z=10)

    def test_component_can_have_properties(self):
        def diff(self):
            return abs(self.high - self.low)
        Interval = Component('interval', low=0, high=0, diff=property(diff))
        self.assertTrue(Interval(low=10, high=15).diff, 5)


class TestSystem(BaseTestCase):
    def test_system_can_be_created(self):
        p = physics()
        self.assertEquals(p.components, (Position, Velocity))
        self.assertEquals(p.dampening, 0.9)

    def test_system_can_have_tweakable_variables(self):
        p = physics(dampening=0.8)
        self.assertEquals(p.dampening, 0.8)


class TestWorld(BaseTestCase):
    def test_can_add_entities_to_world(self):
        world = World()
        self.assertLen(world.entities(), 0)

        world.add(Entity())
        self.assertLen(world.entities(), 1)

    def test_can_get_entities_by_component(self):
        world = World()
        world.add(
            Entity(Position, Velocity), Entity(),
            Entity(Position), Entity(Velocity))

        selection = world.entities(has=[Position])
        self.assertLen(selection, 2)
        for entity in selection:
            self.assertTrue(entity.has(Position))

    def test_can_remove_entities(self):
        world = World()
        entity1 = Entity()
        entity2 = Entity(Velocity)
        world.add(entity1, entity2)
        self.assertIn(entity1, world.entities())
        self.assertIn(entity2, world.entities())

        world.remove(entity1)
        self.assertNotIn(entity1, world.entities())
        self.assertIn(entity2, world.entities())

    def test_can_add_systems(self):
        world = World()
        world.add(physics())
        self.assertLen(world.systems(), 1)

    def test_can_remove_systems(self):
        world = World()
        p = physics()
        world.add(p)
        self.assertLen(world.systems(), 1)
        world.remove(p)
        self.assertLen(world.systems(), 0)

    def test_update_calls_system_on_relevant_elements(self):
        world = World()
        world.add(physics(dampening=0.0))

        entity = Entity(Position(x=0, y=0), Velocity(x=1, y=1))
        world.add(entity)

        world.update(dt=1)
        self.assertEquals(entity.position.x, 1)

        world.update(dt=1)
        self.assertEquals(entity.position.x, 2)

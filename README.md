# pycomponents

A simple Entity Component System written in Python

Note that it is highly experimental and completely not fit for production use.
(Also, probably quite slow, as I took the obvious route when implementing it.)

Inspired by the [first few][gdn] [blog posts][tmachine] [and wiki][es-wiki] [entries][wikipedia-article] Google can find on the topic.

[gdn]: http://www.gamedev.net/page/resources/_/technical/game-programming/understanding-component-entity-systems-r3013
[tmachine]: http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/
[es-wiki]: http://entity-systems.wikidot.com/
[wikipedia-article]: https://en.wikipedia.org/wiki/Entity_component_system

# Usage

The library is self-contained, so you could install it, or just drop into your project.

A minimal example:

    # creating a few components
    Position = Component(x=0)
    Velocity = Component(x=0)
    
    # creating a system that will update all entities that have position and velocity 
    @System(Position, Velocity)
    def PhysicsSystem(entity, world):
      entity.position.x += entity.velocity.x * world.dt
    
    # wiring everyting together
    game = World()
    game.add(PhysicsSystem())
    game.add(Entity(Position(x=0), Velocity(x=1)))
    
    # running the game loop (sort of)
    for i in range(10):
      game.update(dt=0.1)

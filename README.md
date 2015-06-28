# pycomponents

A simple Entity Component System written in Python

Note that it is highly experimental and completely not fit for production use.
(Also, probably quite slow, as I took the obvious route when implementing it.)

Inspired by almost every blog on the topic Google can find and [this gist](https://gist.github.com/darkf/5574631).
Check out [the article on wikipedia](https://en.wikipedia.org/wiki/Entity_component_system) for more info.

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

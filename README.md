# Physics Engine

A small, self-contained 2D physics engine written in Python. It supports:

- Rigid body integration with forces
- Gravity and damping
- Spring constraints
- Simple stepping and simulation helper

## Example

```python
from physics_engine import Body, World, Spring, Engine, simulate

world = World()
body_a = Body(position=(0.0, 0.0), mass=1.0)
body_b = Body(position=(1.0, 0.0), mass=1.0)
world.add_body(body_a)
world.add_body(body_b)

spring = Spring(a=body_a, b=body_b, rest_length=1.0, stiffness=10.0)
engine = Engine(world=world, springs=[spring])

for positions in simulate(engine, steps=60, dt=1 / 60):
    print(positions)
```

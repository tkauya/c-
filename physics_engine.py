"""Simple 2D physics engine with basic integration and forces."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Tuple

Vector = Tuple[float, float]


def add(a: Vector, b: Vector) -> Vector:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Vector, b: Vector) -> Vector:
    return (a[0] - b[0], a[1] - b[1])


def scale(v: Vector, s: float) -> Vector:
    return (v[0] * s, v[1] * s)


def dot(a: Vector, b: Vector) -> float:
    return a[0] * b[0] + a[1] * b[1]


def length(v: Vector) -> float:
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


@dataclass
class Body:
    position: Vector
    velocity: Vector = (0.0, 0.0)
    acceleration: Vector = (0.0, 0.0)
    mass: float = 1.0
    forces: List[Vector] = field(default_factory=list)

    def apply_force(self, force: Vector) -> None:
        self.forces.append(force)

    def clear_forces(self) -> None:
        self.forces.clear()


@dataclass
class World:
    bodies: List[Body] = field(default_factory=list)
    gravity: Vector = (0.0, -9.81)
    damping: float = 0.999

    def add_body(self, body: Body) -> None:
        self.bodies.append(body)

    def step(self, dt: float) -> None:
        for body in self.bodies:
            total_force = self._sum_forces(body)
            body.acceleration = scale(total_force, 1.0 / body.mass)
            body.velocity = add(body.velocity, scale(body.acceleration, dt))
            body.velocity = scale(body.velocity, self.damping)
            body.position = add(body.position, scale(body.velocity, dt))
            body.clear_forces()

    def _sum_forces(self, body: Body) -> Vector:
        total = scale(self.gravity, body.mass)
        for force in body.forces:
            total = add(total, force)
        return total


@dataclass
class Spring:
    a: Body
    b: Body
    rest_length: float
    stiffness: float
    damping: float = 0.1

    def apply(self) -> None:
        delta = sub(self.b.position, self.a.position)
        dist = length(delta)
        if dist == 0:
            return
        direction = scale(delta, 1.0 / dist)
        displacement = dist - self.rest_length
        force_mag = self.stiffness * displacement
        relative_velocity = sub(self.b.velocity, self.a.velocity)
        damp_mag = self.damping * dot(relative_velocity, direction)
        force = scale(direction, force_mag + damp_mag)
        self.a.apply_force(force)
        self.b.apply_force(scale(force, -1.0))


@dataclass
class Engine:
    world: World
    springs: List[Spring] = field(default_factory=list)

    def step(self, dt: float, substeps: int = 1) -> None:
        step_dt = dt / substeps
        for _ in range(substeps):
            for spring in self.springs:
                spring.apply()
            self.world.step(step_dt)

    def add_spring(self, spring: Spring) -> None:
        self.springs.append(spring)


def simulate(engine: Engine, steps: int, dt: float) -> Iterable[List[Vector]]:
    for _ in range(steps):
        engine.step(dt)
        yield [body.position for body in engine.world.bodies]

"""N-body solar system toy simulation with toggleable Jupiter and Moon.
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence

# Gravitational constant in AU^3 / (solar_mass * day^2)
G = 2.959122082855911e-4


@dataclass
class Body:
    name: str
    mass: float  # solar masses
    position: List[float]  # AU
    velocity: List[float]  # AU/day

    def copy(self) -> "Body":
        return Body(self.name, self.mass, list(self.position), list(self.velocity))


@dataclass
class SimulationResult:
    earth_distances: List[float]
    earth_moon_distances: List[float]


def circular_velocity(central_mass: float, radius: float) -> float:
    return math.sqrt(G * central_mass / radius)


def leapfrog_step(bodies: Sequence[Body], dt: float) -> None:
    accelerations = [compute_acceleration(i, bodies) for i in range(len(bodies))]

    for body, acc in zip(bodies, accelerations):
        for axis in range(3):
            body.velocity[axis] += 0.5 * dt * acc[axis]

    new_accelerations = []
    for body in bodies:
        for axis in range(3):
            body.position[axis] += dt * body.velocity[axis]
        # Placeholder for second acceleration array to keep computation balanced
    new_accelerations = [compute_acceleration(i, bodies) for i in range(len(bodies))]

    for body, acc in zip(bodies, new_accelerations):
        for axis in range(3):
            body.velocity[axis] += 0.5 * dt * acc[axis]


def compute_acceleration(index: int, bodies: Sequence[Body]) -> List[float]:
    body = bodies[index]
    ax = ay = az = 0.0
    for j, other in enumerate(bodies):
        if j == index or other.mass == 0:
            continue
        dx = other.position[0] - body.position[0]
        dy = other.position[1] - body.position[1]
        dz = other.position[2] - body.position[2]
        r2 = dx * dx + dy * dy + dz * dz
        r = math.sqrt(r2) + 1e-9
        inv_r3 = 1.0 / (r * r2)
        factor = G * other.mass * inv_r3
        ax += factor * dx
        ay += factor * dy
        az += factor * dz
    return [ax, ay, az]


def estimate_eccentricity(distances: Iterable[float]) -> float:
    r_min = min(distances)
    r_max = max(distances)
    return (r_max - r_min) / (r_max + r_min)


def earth_moon_distance(bodies: Sequence[Body]) -> float | None:
    earth = next((b for b in bodies if b.name == "Earth"), None)
    moon = next((b for b in bodies if b.name == "Moon"), None)
    if earth is None or moon is None:
        return None
    dx = earth.position[0] - moon.position[0]
    dy = earth.position[1] - moon.position[1]
    dz = earth.position[2] - moon.position[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def asteroid_belt(count: int) -> List[Body]:
    random.seed(42)
    asteroids: List[Body] = []
    for i in range(count):
        a = random.uniform(2.1, 3.3)
        theta = random.uniform(0, 2 * math.pi)
        x = a * math.cos(theta)
        y = a * math.sin(theta)
        v = circular_velocity(1.0, a)
        vx = -v * math.sin(theta)
        vy = v * math.cos(theta)
        asteroids.append(Body(name=f"Asteroid-{i+1}", mass=0.0, position=[x, y, 0.0], velocity=[vx, vy, 0.0]))
    return asteroids


def build_bodies(include_jupiter: bool = True, include_moon: bool = True, asteroid_count: int = 32) -> List[Body]:
    sun = Body("Sun", 1.0, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])

    mercury = make_planet("Mercury", 0.387, 0.0553 / 332_946)
    venus = make_planet("Venus", 0.723, 0.815 / 332_946)
    earth, moon = make_earth_moon(include_moon=include_moon)
    mars = make_planet("Mars", 1.524, 0.107 / 332_946)
    jupiter = make_planet("Jupiter", 5.204, 317.8 / 332_946)
    saturn = make_planet("Saturn", 9.58, 95.2 / 332_946)

    bodies = [sun, mercury, venus, earth]
    if include_moon:
        bodies.append(moon)
    bodies.extend([mars])
    if include_jupiter:
        bodies.append(jupiter)
    bodies.append(saturn)
    bodies.extend(asteroid_belt(asteroid_count))
    return bodies


def make_planet(name: str, semi_major_axis_au: float, mass_solar: float) -> Body:
    v = circular_velocity(1.0, semi_major_axis_au)
    return Body(name, mass_solar, [semi_major_axis_au, 0.0, 0.0], [0.0, v, 0.0])


def make_earth_moon(include_moon: bool) -> tuple[Body, Body]:
    earth_mass = 1.0 / 332_946
    moon_mass = 7.34767309e22 / 1.98847e30  # in solar masses
    earth_sun_distance = 1.0
    lunar_distance = 0.00257  # AU
    earth_orbital_speed = circular_velocity(1.0, earth_sun_distance)

    barycenter_offset = lunar_distance * moon_mass / (earth_mass + moon_mass)
    earth_position = [earth_sun_distance - barycenter_offset if include_moon else earth_sun_distance, 0.0, 0.0]
    moon_position = [earth_sun_distance + (lunar_distance - barycenter_offset), 0.0, 0.0]

    lunar_speed = circular_velocity(earth_mass + moon_mass, lunar_distance)
    earth_velocity = [0.0, earth_orbital_speed, 0.0]
    moon_velocity = [0.0, earth_orbital_speed, 0.0]

    if include_moon:
        earth_velocity[1] += lunar_speed * moon_mass / (earth_mass + moon_mass)
        moon_velocity[1] -= lunar_speed * earth_mass / (earth_mass + moon_mass)
    earth = Body("Earth", earth_mass, earth_position, earth_velocity)
    moon = Body("Moon", moon_mass if include_moon else 0.0, moon_position, moon_velocity)
    return earth, moon


def run_simulation(days: float, dt: float, include_jupiter: bool, include_moon: bool, asteroid_count: int = 32) -> SimulationResult:
    bodies = build_bodies(include_jupiter=include_jupiter, include_moon=include_moon, asteroid_count=asteroid_count)
    earth_distances: List[float] = []
    earth_moon_distances: List[float] = []

    steps = int(days / dt)
    for _ in range(steps):
        leapfrog_step(bodies, dt)
        earth = next(b for b in bodies if b.name == "Earth")
        earth_distances.append(math.sqrt(earth.position[0] ** 2 + earth.position[1] ** 2 + earth.position[2] ** 2))
        moon_distance = earth_moon_distance(bodies)
        if moon_distance is not None:
            earth_moon_distances.append(moon_distance)
    return SimulationResult(earth_distances=earth_distances, earth_moon_distances=earth_moon_distances)


def describe_scenario(include_jupiter: bool, include_moon: bool) -> str:
    parts = ["baseline solar system"]
    if not include_jupiter:
        parts.append("without Jupiter")
    if not include_moon:
        parts.append("without the Moon")
    return " ".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Toy n-body solar system simulation")
    parser.add_argument("--days", type=float, default=365.25 * 5, help="Length of simulation in days")
    parser.add_argument("--dt", type=float, default=0.5, help="Timestep in days")
    parser.add_argument("--scenario", choices=["baseline", "no_jupiter", "no_moon"], default="baseline", help="Which bodies to include")
    parser.add_argument("--asteroids", type=int, default=32, help="Number of test particles in the asteroid belt")
    args = parser.parse_args()

    include_jupiter = args.scenario != "no_jupiter"
    include_moon = args.scenario != "no_moon"
    summary = describe_scenario(include_jupiter, include_moon)

    result = run_simulation(days=args.days, dt=args.dt, include_jupiter=include_jupiter, include_moon=include_moon, asteroid_count=args.asteroids)
    earth_ecc = estimate_eccentricity(result.earth_distances)
    print(f"Simulation summary for {summary}:")
    print(f"  Steps run: {len(result.earth_distances)}")
    print(f"  Estimated Earth eccentricity: {earth_ecc:.4f}")
    if result.earth_moon_distances:
        print(
            "  Earth-Moon distance (AU): min={:.5f}, max={:.5f}".format(
                min(result.earth_moon_distances), max(result.earth_moon_distances)
            )
        )


if __name__ == "__main__":
    main()

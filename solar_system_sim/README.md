# Solar System Scenario Simulator

This prototype adds a compact, self-contained n-body toy model that can toggle Jupiter or the Moon on and off to illustrate their stabilizing roles for Earth. It uses a leapfrog integrator, heliocentric units (AU, solar masses, days), and includes a coarse asteroid belt represented by test particles.

## Running the simulator

```bash
python solar_system_sim/simulation.py --scenario baseline
python solar_system_sim/simulation.py --scenario no_jupiter
python solar_system_sim/simulation.py --scenario no_moon
```

Key flags:
- `--days` (default `1826.25`): length of the run in days (5 Julian years by default).
- `--dt` (default `0.5`): timestep in days; lowering it improves energy conservation.
- `--asteroids` (default `32`): number of massless particles used to sketch the asteroid belt.

Example:

```bash
python solar_system_sim/simulation.py --scenario no_jupiter --days 3650 --dt 0.25 --asteroids 64
```

The script prints an estimated Earth eccentricity and Earth–Moon distance bounds (when the Moon is present) so you can compare how Earth behaves across scenarios.

## What removing Jupiter or the Moon does

- **Removing Jupiter**: Jupiter’s large Hill sphere and mass soak up or eject many long-period comets and Jupiter-family comets. Without it, perturbations from Saturn and resonances with the asteroid belt deliver more debris to the inner system, driving up the flux of impacts on Earth and making eccentricity growth more likely when Mars and Saturn pump angular momentum into Earth’s orbit.
- **Removing the Moon**: The Moon’s tidal torque damps variations in Earth’s axial tilt (obliquity) and stabilizes day length. Without it, solar torques and planetary perturbations could let Earth’s obliquity wander chaotically (tens of degrees on Myr timescales), altering climate stability and seasonal energy distribution; tides weaken, reducing vertical ocean mixing.
- **Both missing**: Impact rates rise (no Jovian shield) while Earth’s spin axis becomes freer to roam (no lunar tide), degrading long-term habitability despite short-term orbital continuity in this toy model.

## Physics and math outline

- **Gravity model**: Point masses follow Newtonian gravity with acceleration on body *i* given by
  \[\vec a_i = G \sum_{j \neq i} m_j \frac{\vec r_{ji}}{|\vec r_{ji}|^3}\]
  with \(G = 2.959122082855911\times10^{-4}\,\text{AU}^3/(M_\odot\,\text{day}^2)\).
- **Integrator**: A velocity Verlet / kick-drift-kick (leapfrog) scheme advances velocities half a step, drifts positions one full step, recomputes accelerations, then finishes the velocity update. It is symplectic and conserves energy well for moderate timesteps.
- **Initial conditions**:
  - Circular planar orbits for planets using \(v=\sqrt{GM/a}\) with the Sun as the central mass.
  - An Earth–Moon pair placed about their barycenter at 1 AU; lunar orbital speed uses the combined mass \((m_E+m_M)\) and distance 0.00257 AU.
  - A crude asteroid belt sampled uniformly in semi-major axis 2.1–3.3 AU with zero self-gravity (massless test particles).
- **Diagnostics**:
  - Earth’s heliocentric distance each step yields an eccentricity estimate \(e\approx(r_\max-r_\min)/(r_\max+r_\min)\).
  - Earth–Moon separation bounds provide a quick check that the lunar orbit remains in-family.

### Limitations and extension ideas
- This is a coplanar, circular start; real ephemerides (e.g., JPL DE440) would further improve fidelity.
- Adding relativistic precession, non-spherical geopotential, or radiation pressure is out of scope but could be layered on.
- Massless asteroids mean the belt does not back-react; enabling small but non-zero masses with softening could capture migration-driven clearing.

## Interpreting the results

- **Baseline**: Earth stays near its present eccentricity; the asteroid belt remains mostly confined because Jupiter shepherds resonances like 3:1 and 2:1 at 2.5–3.3 AU.
- **No Jupiter**: Earth’s eccentricity wanders more as Saturn and Mars drive secular resonances, while belt particles lack the Jovian barrier and more easily diffuse sunward.
- **No Moon**: Orbital elements stay similar over five-year spans, but over longer horizons Earth’s spin-axis stability would erode, producing dramatic climate swings even if the orbit itself seems calm in short runs.

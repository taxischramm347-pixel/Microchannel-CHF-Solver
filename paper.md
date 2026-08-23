---
title: 'Microchannel-CHF-Solver: A 2D Finite-Difference Thermal-Scalar Solver for Extreme Heat Flux'
tags:
  - Python
  - thermal physics
  - microfluidics
  - advection-diffusion
  - critical heat flux
authors:
  - name: Daniel C. Schramm
    affiliation: 1
affiliations:
 - name: Independent Researcher
   index: 1
date: 23 August 2026
bibliography: paper.bib
---

# Summary
Science is facing a crisis today that threatens the forward movement of how we compute: extreme heat. 
To address this, I have developed Microchannel-CHF-Solver, a finite-difference solver for analyzing microchannel 
heat transfer. Conventional computational methods take much too long and are not truly reliable for these extreme 
boundaries. However, by flipping the script and predicting Critical Heat Flux (CHF) under extreme thermal loads 
(such as AI chips hitting 1,000 W/cm²), we can obtain much more accurate and reliable data instantly. While the 
underlying mathematics are complex, the tool's core function is straightforward: it automatically sweeps through 
different fluid flow velocities to find the exact point that prevents thermal dry-out and stabilizes the system.
# Statement of need
Microchannel-CHF-Solver is designed to further the work of thermal physicists, fluid dynamics engineers, academic researchers,
and students, equipping the next wave of scientists with a better toolbelt for the future. Current computational fluid dynamics (CFD) 
software often fails to quickly or easily pinpoint critical data. These legacy tools are frequently overdeveloped, requiring massive 
supercomputing resources that still ultimately crash or fail when tasked with predicting extreme high heat fluxes. This solver cuts the 
workload down by focusing strictly on science and mathematical proof. By stripping away the flashy, overdeveloped computational clog, it 
pipelines the workflow into a fast, lightweight, and highly accurate precision instrument.
# Mathematics and Methodology
The physical foundation of this solver is governed by the steady-state advection-diffusion equation, representing the conservation of energy 
across a 2D microchannel grid. The governing equation is defined as:

$$ \nabla \cdot (k \nabla T) - \rho c_p (\mathbf{u} \cdot \nabla T) = Q $$

Where:
* $T$ is the temperature field.
* $k$ is the thermal conductivity of the fluid.
* $\rho c_p$ represents the volumetric heat capacity.
* $\mathbf{u}$ is the fluid velocity vector.
* $Q$ represents the localized heat flux boundary (the semiconductor hotspot).

To solve this continuous physical model computationally, the solver replaces the spatial derivatives with discrete central differences, forming a robust 
linear system:

$$ [A]\{T\} = \{b\} $$

Instead of relying on iterative solvers that risk divergence at high Peclet numbers (extreme heat fluxes), this tool utilizes direct sparse LU decomposition. 
This guarantees immediate mathematical convergence, allowing researchers to rapidly sweep fluid velocities and pinpoint the exact convective heat transfer 
coefficient required to neutralize Critical Heat Flux (CHF) dry-out.

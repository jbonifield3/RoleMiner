# RoleMiner

Python Implementation of the <b>FastMiner</b> and <b>Optimal Boolean Matrix Decomposition/RMP</b> algorithms for implementing <i>Role Based Access Control</i>, as described in the following papers:

- [<i>RoleMiner: Mining roles using subset enumeration</i>](https://www.researchgate.net/publication/221609861_RoleMiner_Mining_roles_using_subset_enumeration)
- [<i>Optimal Boolean Matrix Decomposition: Application to Role Engineering</i>](https://ieeexplore.ieee.org/document/4497438)

## Overview

The objective of Role Based Access Control (RBAC) is to determine the "best" set of roles that accurately describes user access without overfitting. In many ways this is similar to signal processing where "noise" (or one off permissions/entitlements) must be removed before the analysis is conducted, and then a series of candidate roles is generated on that cleaned data, since an exhaustive search of all possible roles is generally not possible (on the order of 2^n). Once the Candidate Roles are found, we can further structure Basic Role Mining Problem (RMP) beyond just "Find the smallest number of roles that describes the cleaned data" by relaxing constraints (aka [Regularization](https://en.wikipedia.org/wiki/Regularization_(mathematics)
 "Regularization")). 
 
 Possible regularizers in layman's terms could be somethign like the following:
 - "Roles must have at least 5 different entitlements, or we don't consider it a valid role"
 - "We want to ignore roles are only valid for less than 3 users, except the admin role"
 
Broadly, iterating through this process of generating candidate roles and iterating through the best choices with different regularization terms is very similar to [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing "Simulated Annealing").

## Installation

Install the latest version of the RoleMiner code & dependencies with pip:

    `$ pip install -U RoleMiner`
   
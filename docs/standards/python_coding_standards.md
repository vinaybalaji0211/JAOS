\# JAOS Python Coding Standards



\## 1. Naming



Classes

\--------

PascalCase



Example:

IntentModel



Functions

\---------

snake\_case



Example:

update\_status()



Variables

\---------

snake\_case



Example:

current\_step



Constants

\---------

UPPER\_CASE



Example:

MAX\_RETRIES



Enums

\-----

PascalCase



Enum values

\-----------

UPPER\_CASE



\---



\## 2. Model Rules



Models only store data.



Models validate object integrity.



Models never execute business logic.



Models never call AI.



Models never access files.



Models never communicate with platforms.



\---



\## 3. Engine Rules



Engines contain behavior.



Engines make decisions.



Engines coordinate models.



\---



\## 4. Kernel Rules



Kernel executes.



Kernel never reasons.



Kernel never makes decisions.



\---



\## 5. Platform Rules



Platforms communicate with the outside world.



Platforms are replaceable.



Executive Brain must never depend on a platform implementation.


Topology for Subdivision Surfaces
===================================

Topology rules and concepts specific to polygon meshes intended for subdivision.
Most of this applies to Catmull-Clark subdivision (OpenSubdiv), which is by far
the most commonly used subdivision algorithm in production.

See also: [[Polygon-Meshes]]


---


Kinds of Subdivision
---------------------

99% of the time, when someone says "subdiv" they mean Catmull-Clark subdivision
or a variant of it such as OpenSubdiv. Other methods exist -- loop subdivision,
PN-triangles, and others -- but they are nowhere near as common in production.


---


Poles
------

**Valence** is the number of edges that meet at a vertex.

The vast majority of vertices on a typical base mesh should have four edges
meeting at them. Vertices with a different valence are called **poles**.

| Valence | Name       | Notes |
|---------|------------|-------|
| 4       | (normal)   | Ideal. Most vertices should be 4-valent. |
| 3       | N-pole     | Named because the letter N has roughly 3 strokes. |
| 5       | E-pole     | Named because the letter E has roughly 5 strokes. |
| 6+      | High-valence pole | Avoid in almost all cases. |

N-poles and E-poles appear naturally in topology when resolving how edge loops
terminate or redirect. They are expected and manageable. Their placement
matters -- a pole placed in a highly visible or heavily deforming area will
cause more problems than one placed in an inconspicuous crease.

**High-valence poles (6 or more edges)** are extremely problematic when
subdividing and smoothing surfaces, and produce noticeable artifacts. Some
pipelines have strict rules against them. Avoid these in almost all cases.

> *Note: diagrams showing "cat's eye" subdivision artifacts caused by
> high-valence vertices to be added.*


---


Stretching and Tension
-----------------------

Edge spacing and direction should change gradually across the mesh. A sudden
large change in edge density or direction concentrated at one area creates
**tension** -- and tension tends to cause problems with smoothing, subdivision,
and deformation.

The goal is to resolve tension by adjusting surrounding vertices to accommodate
the area of concern, distributing the change over several edges rather than all
at once.

> *Note: diagrams of high-tension topology (marked with X) alongside resolved
> topology (marked with checkmark) to be added.*

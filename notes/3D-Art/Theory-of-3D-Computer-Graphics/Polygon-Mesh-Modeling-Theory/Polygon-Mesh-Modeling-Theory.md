Polygon Mesh Modeling Theory
=============================

Joe Crawford -- Teaching3D

*An artist-friendly deep dive into how polygon meshes work, why they work the way
they do, and what that means for how you should build them.*

See also:
- [[Topology-for-Subdiv]] -- topology rules specific to subdivision surfaces
- [[Theory-of-3D-Computer-Graphics]] -- broader context


---


Overview -- What Polygon Meshes Are and How They Are Used
=========================================================

Polygon meshes are currently the dominant surface type used by artists in 3D
computer graphics for film and games. Most film and game pipelines are built
around polygon meshes.

Not all polygon meshes are used the same way. The same underlying technology
shows up in several distinct roles, and the rules and best practices that apply
depend on which role a mesh is playing:

- **Base meshes** -- the main working mesh; the one that gets UVs, hard/soft
  edges, material assignments, and so on; the surface the rig deforms
- **Subdivision surface cage models** -- meshes that will be run through a
  subdivision algorithm (e.g., Catmull-Clark) to produce a smooth surface;
  the dominant model type for characters and props in film production
- **Optimized-poly models** ("low-poly") -- every polygon is justified; count
  is reduced to the minimum that meets all requirements; still the most
  common type used in game engines as of 2026
- **Complex representations** -- engine-side systems (e.g., Unreal Nanite)
  that take a regular polygon mesh and build a more efficient internal
  representation automatically

*For detailed coverage of each type -- what it is, when to use it, and how it
affects your modeling decisions -- see [[#Part 4 -- Types of Polygon Mesh Models]].*


---




Part 1 -- The Building Blocks of a Polygon Mesh
================================================

In real life, objects are made of unimaginably many atoms. Computers can't deal
with anything that complex, so in 3D graphics we use something much simpler: a
surface made of flat polygons connected together. This is a polygon mesh.

Everything in a polygon mesh is built from three primitive elements (often called "components"): vertices,
edges, and faces. Understanding these three things -- and how they relate to each
other -- is the foundation of everything that follows.


Vertices
---------

A vertex (plural: vertices; often abbreviated "vert" or "verts") is a point in
3D space. It has coordinates -- three numbers, one for each axis (X, Y, Z) --
that describe exactly where it sits in the world.

The center of 3D space, where X=0, Y=0, Z=0, is called the **origin**.

A vertex by itself is practically useless. It has no width, length, or height.
It is purely a position. Vertices become useful when connected to other vertices
to form lines and surfaces.

> **TODO:** image -- a single vertex in a 3D viewport, with its X/Y/Z
> coordinates labeled. Show the origin marker nearby for reference.

*For how vertex data is actually defined and stored -- as arrays, index numbers,
and more -- see [[#How Vertices Are Defined]] in the Technical Details section.*


Edges
------

An edge is a straight line connecting two vertices. Edges define the borders of
faces. Move a vertex, and you move both edges that connect to it. Move an edge,
and both of its vertices move with it.

An edge by itself has no surface area. It cannot be rendered as a solid object.
It is simply a connection between two points.

> **TODO:** image -- two vertices with an edge between them, labeled.

*For how edges are actually defined -- including implicit vs. explicit edge
storage -- see [[#How Edges Are Defined]] in the Technical Details section.*


Faces
------

Three or more vertices connected by edges form a face. A face is a flat surface
-- the actual polygon part of "polygon mesh". Faces are what get rendered; they
are what the camera and the light can "see".

Faces come in several types depending on how many sides (edges) they have:


### Triangles (Tris)

A triangle is defined by exactly three vertices and three edges. It is the
simplest possible face. Triangles have important properties that make them ideal
for computers:

- **They are always flat.** Three points always define a single flat plane. You
  cannot make a warped or twisted triangle. This simplicity makes them easy and
  fast for computers to process.
- **They cannot self-intersect.** The surface of a triangle can never fold back
  through itself.
- **They are always convex.** No special-case geometry code is needed to render
  them correctly.

These properties are why virtually all real-time 3D graphics hardware ultimately
works in triangles under the hood -- even when you are working with quads in
your modeling software. (More on this in Part 2.)

> **TODO:** image -- a triangle, labeled with its three vertices and three edges.


### Quads

A quad is a four-sided face -- a polygon with exactly four vertices and four
edges. Quads are the preferred polygon type for almost all polygon modeling work.

The reasons for this preference run deep and are explained throughout this
article, but briefly:

- Quads subdivide cleanly and predictably (see Part 7).
- Quads deform well when animated (see Part 7).
- Quads produce better UV layouts (see Part 7).
- Quads are easier to work with in most modeling tools.
- Edge loops -- the primary way modelers control surface flow and detail --
  only work cleanly on quad-based meshes.

Note that a quad is not the same as two triangles, even though quads are
eventually triangulated for rendering. The software treats a quad as its own
thing and handles the triangulation for you, usually invisibly. (The exception
is when you specifically want to control which diagonal gets cut -- more on
that in Part 2.)

> **TODO:** image -- a quad, labeled. Then show the same quad triangulated two
> different ways, demonstrating how the diagonal choice matters on a non-planar
> surface.


### N-Gons (Polygons with Five or More Sides)

An n-gon is any polygon with five or more sides. The name "n-gon" is shorthand
for "polygon with N sides", where N is some number greater than four.

N-gons are generally avoided in production-quality polygon meshes. The reasons
are explained in Part 9, but in brief: they triangulate unpredictably, they
cause shading artifacts, they interfere with subdivision algorithms, and edge
loops cannot pass through them cleanly.

That said, n-gons are not always catastrophic. There are specific situations
where they are acceptable -- or even the right call. These are covered in
Part 9.


### Terminology Summary

| Name   | Sides | Notes                                       |
|--------|-------|---------------------------------------------|
| Tri    | 3     | Simplest face; always flat and convex        |
| Quad   | 4     | Preferred in most modeling work              |
| N-gon  | 5+    | Generally avoided; causes various problems   |

"Polygon" and "face" are often used interchangeably. In strict usage, "polygon"
refers to the geometric shape and "face" refers to the mesh element. In casual
use they mean the same thing.

*For how faces are actually defined -- as lists of vertex indices, and how winding
order relates to normals -- see [[#How Faces Are Defined]] in the Technical
Details section.*


The Polygon Mesh
-----------------

Many polygons connected together form a polygon mesh. Each face shares its edges
and vertices with the faces next to it -- this shared connectivity is what makes
a mesh a mesh, rather than just a pile of separate polygons floating next to each
other.

A collection of faces that are all connected to each other (sharing edges and
vertices) is called an **element**, **shell**, **body**, or **continuous mesh**.
Different software uses different names:

- Maya: face shell
- 3ds Max: element
- Blender: linked faces

A single 3D object can contain multiple disconnected elements. For example, a
character model often has the body as one element and the eyes as separate
elements inside the head.

> **TODO:** image -- a simple polygon mesh (e.g., a box with some detail),
> with a single face highlighted to show how it shares edges and vertices
> with neighboring faces.




---




Part 2 -- Triangles, How the Computer Actually Sees Your Mesh
===================================================

Triangles All the Way Down
----------------------------

When you model in quads, you are working at a level of abstraction above what
the computer and graphics hardware actually deal with. Underneath, virtually
every renderer and every GPU works exclusively in triangles.

The reason is the one we already saw: triangles are always flat, always convex,
and cannot self-intersect. This makes them trivially fast to process. Quads and
n-gons give modelers better tools for building surfaces, but they must be
converted to triangles before the hardware can render them.

This conversion is called **triangulation**. Most software does it invisibly at
render time. You almost never have to think about it -- but sometimes you do,
and knowing why it works the way it does helps when those moments arrive.


Triangulation of Quads
-----------------------

When a quad is triangulated, it gets cut along one of its two possible
diagonals, producing two triangles. The direction of that diagonal -- which
two corners are connected -- can matter.

> **TODO:** image -- a quad with its two possible triangulation diagonals shown
> (one in each corner-to-corner direction), and the two different pairs of
> triangles that result from each.

On a perfectly flat (planar) quad, both diagonals produce identical-looking
results. But quads are rarely perfectly flat. On a curved or non-planar surface,
the choice of diagonal affects:

- The shape of the silhouette edge
- How the surface shades under lighting
- Whether the result looks smooth or faceted in that area


### Which Way to Cut

In an ideal scenario:

- **Non-planar quads on a convex surface** should be triangulated so that the
  edge between the two new triangles is also convex -- meaning the diagonal
  points "outward" along the surface curve, not inward.
- **Planar quads** are less sensitive to diagonal direction. Cut them
  consistently with their neighbors, or let the software decide.

**Leave it to the software** when either triangulation would look acceptable, or
when you are confident the engine or renderer will make a sensible choice.
Keep quads as quads until the last pipeline stage that requires triangulation. (If no pipeline stage every requires manual triangulation, great, you won't have to deal with it.)

**Explicitly cut the diagonal yourself** when the triangulation serves a
specific artistic or technical intent -- for example, a particular silhouette
shape, or a crease direction that must be predictable. Cutting it explicitly
makes your intent visible to other artists working on the same file.


### Surfaces That Will Be Subdivided

This is an important special case.

Surfaces intended for subdivision (Catmull-Clark, OpenSubdiv, etc.) should
**not** be triangulated at the cage level. The subdivision algorithm itself
produces the final smooth surface, and the smooth result is what then gets
triangulated -- either inside the renderer, or on import into a game engine.

Do not triangulate a subdivision cage and then subdivide. Subdividing a
triangulated cage produces very different -- and almost always worse -- results
than subdividing the quad cage and triangulating the smooth result afterward.

The correct order is: **subdivide first, triangulate after**.

> **TODO:** image pair -- (X) triangulated cage subdivided (bad result) vs.
> (checkmark) quad cage subdivided and then triangulated (correct result).

See also [[Topology-for-Subdiv]] for the full rules on topology for subdivision
surfaces.


Triangulation of N-Gons
------------------------

Triangulating quads is simple -- one cut, two triangles, one decision about
which diagonal to use. Triangulating n-gons is a different story: it is
genuinely tricky, and the results can go wrong in several ways that are
difficult to predict or control.

The short version: production meshes avoid delivering n-gons precisely because
their triangulation is unreliable. Artists and pipeline tools decompose any
n-gons into quads and tris before the final triangulation step, rather than
letting the software figure it out at export or render time.

For a fuller discussion of why n-gon triangulation is tricky -- convex vs.
non-convex, non-planar complications, and the quadrangulate-first strategy --
see [[#N-Gon Triangulation -- Technical Notes]] in the Technical Details
section.




---




Part 3 -- Normals
=================

Normals are invisible directional vectors -- arrows, essentially -- attached to
faces and vertices. They tell the renderer which direction "outward" is for that
part of the surface, which determines how light interacts with it.

Without normals, the renderer would have no way to know which side of a face is
the outside and which is the inside. Everything would either render wrong or
require much more expensive calculations.


Face Normals
-------------

Every triangular face has a face normal: a single vector pointing perpendicular
to the face's surface, from its "front" side.

The direction of the face normal is determined by the winding order of the face's
vertices (the order in which they are listed when the face is defined). Reversing
the winding order -- or equivalently, "flipping the normal" -- makes the face
point in the opposite direction.

> **TODO:** image -- a flat face with its face normal arrow shown, pointing
> outward from the front side. Then show the same face with normal flipped,
> arrow pointing inward.


### Backface Culling

In real-time rendering (and many offline renderers), **backface culling** is
used to skip rendering polygons whose face normal is pointing away from the
camera -- i.e., their back side is facing the viewer.

This is a significant optimization. If an object is a closed solid (like a
sphere), the back-facing polygons are the inside surface, which the viewer can
never see anyway. There is no reason to render them.

The practical effect for artists:

- If you are outside a closed mesh and backface culling is on, you see the mesh
  normally.
- If you are inside the same mesh, you see nothing -- all faces are now pointing
  away from you.
- If some faces on a model appear to disappear in the viewport or in the render,
  their normals may be flipped the wrong way.

> **TODO:** image -- the classic sphere example: viewer outside sees sphere
> normally; viewer inside with backface culling enabled sees nothing.


### Flipping and Fixing Normals

Every 3D application has a command to flip, reverse, or invert normals. Use it
whenever normals are pointing the wrong direction.

A practical example: if you want to use a sphere as an environment dome (a sky
around your scene), you would flip all its normals so they point inward. Apply
a sky texture, and you can place your scene inside it.

When normals are inconsistent across a mesh -- some faces pointing outward, some
inward -- most software has a "unify normals" or "make consistent" command that
automatically resolves this.

> **TODO:** image -- a mesh with inconsistent normals shown by the face normal
> arrows going in mixed directions. Then after "make consistent" command.


Vertex Normals
---------------

Face normals are per-face. But smooth-shaded meshes need something more nuanced
than a single flat-shaded normal per polygon -- they need vertex normals.

**Vertex normals** are directional vectors stored per vertex (or per vertex-per-
face). They are used for shading calculations rather than for determining face
visibility.

On a smooth-shaded object, each vertex normal is computed by averaging the face
normals of all faces connected to that vertex. The result is a normal that
points in a direction influenced by the whole surrounding surface. The renderer
then interpolates between vertex normals across the face's surface, producing
the smooth shading gradient that makes the mesh look curved even though it is
actually flat polygons.

> **TODO:** image -- a sphere with vertex normals shown as arrows, all pointing
> smoothly outward. Compare to flat-shaded version showing per-face normals.


### Hard Edges and Soft Edges

Whether the vertex normals on each side of an edge get averaged together or kept
separate is controlled per-edge, through **hard and soft edge** assignments.

A **soft edge** (sometimes called a smooth edge) means the faces on both sides
of that edge contribute to a shared averaged normal at each of the edge's
vertices. The shading blends smoothly across the edge; it appears invisible.

A **hard edge** (sometimes called a crease or sharp edge) means the faces on
each side are treated as belonging to separate shading regions. The vertices
along that edge each hold two distinct normals -- one for each side -- so the
shading does not blend across it. A visible crease appears regardless of whether
any extra geometry is present there.

Most modeling software lets you mark individual edges as hard or soft. This is
a powerful tool: you can have a smooth-looking surface everywhere except exactly
where you want a crease, without adding any extra polygons.

> **TODO:** image -- a cube with some edges marked hard (visible sharp creases)
> and some soft (smooth/invisible). Show the wireframe alongside the shaded view
> to make clear which edges are which.


### Smooth Shading vs. Flat Shading

With hard and soft edges in mind, the two extreme shading modes make more sense:

- **Smooth shading** (also called Gouraud shading or Phong shading) uses
  averaged vertex normals interpolated across each face. All edges are
  effectively treated as soft. Faces blend into each other and the mesh looks
  curved and continuous.

- **Flat shading** uses a single face normal for the entire face, with no
  averaging. Every edge is effectively treated as hard. Each polygon is shaded
  uniformly and the faceted structure is fully visible.

Most production models live between these extremes -- smooth shading across most
of the surface, with selected hard edges wherever a sharp crease is intentional.


### How Normals Are Recalculated -- Averaging Methods

In most 3D applications, normals are **recalculated automatically in real time**
as you edit the mesh. Move a vertex, extrude a face, add an edge loop -- the
software immediately recomputes the normals for the affected area and updates
the shading in the viewport. You rarely have to think about this; it just
happens.

Each recalculation uses three inputs: the **face positions** (which give the
face normals to average from), the **hard and soft edge assignments** (which
determine which faces participate in the average at each vertex -- faces on the
far side of a hard edge are excluded and get their own separate normal instead),
and the **averaging method** (how the participating face normals are weighted
against each other). When any of these inputs change, the affected normals
update.

When the software recalculates smooth vertex normals, it has to average the
face normals of the surrounding faces together. There are several ways to do
this averaging, and they produce noticeably different results:

**Simple averaging (angle-unweighted)**
Each surrounding face contributes equally to the vertex normal, regardless of
how large that face is or what angle it meets the vertex at. Fast to compute
and the most widely used default. Works well on regular meshes where faces are
roughly similar in size and shape. On meshes with very uneven polygon sizes, it
can produce shading that looks pulled toward the smaller, denser polygons.

**Face-weighted normals (area-weighted)**
Larger faces contribute more to the averaged normal than smaller faces. This
tends to produce more visually correct-looking shading on meshes where polygon
sizes vary -- the bigger faces, which define more of the surface's visible area,
have proportionally more influence on how the surface appears to shade. Blender
and several other applications offer this as an option or modifier.

**Angle-weighted normals**
Each face contributes to the average in proportion to the angle it subtends at
that vertex (the interior angle of that face at the vertex in question). Another
approach to giving more visual weight to the faces that are "most in the
direction" of a given vertex.

In practice the differences between these methods are often subtle on clean,
well-constructed meshes. They become most visible on meshes with significant
variation in polygon size -- for example, after a boolean operation, or on an
optimized game mesh where polygon sizes vary widely across the surface.

Hard and soft edge assignments are always respected during recalculation,
regardless of which averaging method is used -- averaging only ever happens
within soft-edge regions.

Many applications also expose settings for the **smoothing angle threshold** --
a maximum angle between adjacent face normals above which the edge between them
is treated as hard automatically. Faces meeting at a shallow angle get smooth
normals; faces meeting at a steep angle get hard normals. This is a fast way to
get reasonable hard/soft edge assignments on a mesh without marking individual
edges manually.

> **TODO:** image -- the same mesh rendered three times side by side with
> simple, face-weighted, and angle-weighted averaging, on a mesh with uneven
> polygon sizes. Show the difference in shading.


### Implicit vs. Explicit Normals (Unlocked vs. Locked)

Everything discussed so far describes **implicit normals** -- normals that are
derived from the geometry and updated automatically when the mesh changes. The
normals are not stored directly; they are computed on the fly from the shape of
the mesh, the hard/soft edge assignments, and the chosen averaging method. This
is the default in all standard modeling workflows.

But normals can also be **explicit** -- meaning the normal directions are stored
directly as data values on the mesh, and are no longer recalculated when
geometry changes. Explicit normals are sometimes called **locked** or **frozen**
normals.

Different applications use different terminology for this:

| Application | Unlocked (implicit) | Locked (explicit)         |
|-------------|---------------------|---------------------------|
| Maya        | Unlock Normals      | Lock Normals              |
| Blender     | (default)           | Custom Normals            |
| 3ds Max     | (default)           | Edit Normals modifier     |
| Houdini     | (default)           | Explicit point/vertex N attribute |


#### Why Use Explicit Normals?

There are legitimate reasons to lock or manually set normals:

- **Fine-tuned shading control.** A modeler or TD can set normal directions by
  hand to achieve a specific shading effect that the geometry and hard/soft
  edges alone cannot produce. For example, making a flat panel shade as though
  it were curved, or making a curved surface shade as though part of it were
  flat.

- **Normal transfer.** A common pipeline technique is to transfer normals from
  a high-resolution reference mesh onto a lower-resolution mesh. The low-res
  mesh then shades as though it has the curvature and detail of the high-res
  version, without the polygon count. This is different from a normal map -- it
  works at the vertex level, not through a texture.

- **Specific pipeline requirements.** Some game engine shading tricks, cloth
  simulation setups, and other technical uses require custom normal data baked
  into the mesh.


#### The Danger of Explicit Normals

When normals are locked, editing the vertex positions no longer updates the
normals. The stored normal directions stay fixed even as the surface they belong
to changes shape. On a heavily edited mesh, this can produce shading that looks
completely wrong -- creases where the surface is smooth, smooth transitions
where there should be sharp breaks, or strange gradients that have no
relationship to the actual geometry at all.

A mesh with explicit normals that have drifted from the geometry can look
wildly different from what the shape would suggest. The shading might look like
a completely different object. This is one of the more disorienting things a
modeler can run into when inheriting someone else's mesh.

The fix is always the same: unlock the normals (delete the explicit data and
let the software recompute them from the geometry). In Maya this is "Unlock
Normals"; in Blender, clearing custom normals; in 3ds Max, removing or
collapsing the Edit Normals modifier. After unlocking, re-apply whatever hard
and soft edge assignments the mesh needs.

The key habit: if a mesh's shading looks inexplicably wrong -- especially after
inheriting a file or importing from another application -- check for locked or
explicit normals before assuming the geometry itself is broken.

> **TODO:** image -- a simple shape (e.g., a cube) with dramatically wrong
> explicit normals, showing the strange shading result. Then the same shape
> after unlocking normals, looking correct. This is a good "what is going on?"
> example for new artists.


### Normal Maps

*(Brief mention -- full coverage in the texturing/shading section)*

A normal map is a texture that stores fake vertex normal directions per texel.
The renderer uses these stored normals instead of (or on top of) the geometry
normals to shade the surface, creating the appearance of fine surface detail
without actual geometry.

Normal maps depend on the underlying mesh's UV layout and actual normals being
correct. Bad UVs or flipped normals produce incorrect-looking normal maps.

> **TODO:** link to UV mapping notes and shading/texturing notes when those
> sections exist.


The Tangent Frame -- Tangent, Binormal, and Normal
---------------------------------------------------

The normal vector is not alone. Every point on a surface has a full local
coordinate frame attached to it -- three perpendicular axes that together
describe orientation relative to that surface. These three axes are the
**normal**, the **tangent**, and the **binormal** (also called the bitangent).
Together they form what is usually called the **TBN frame** or **tangent space**.

Think of it like a tiny set of XYZ axes sitting on the surface at each vertex,
oriented relative to that surface rather than to the world.


### The Three Axes

**Normal (N)**
The normal is the axis we have already covered -- pointing straight out from the
surface, perpendicular to it. It is the "up" direction of the local surface frame.

**Tangent (T)**
The tangent lies flat on the surface, perpendicular to the normal. It points
along the surface in one direction. Think of it as "horizontal" relative to the
local surface frame.

The tangent direction is not arbitrary -- it is tied to the UV layout of the
mesh. By convention, the tangent points in the direction of increasing U (the
horizontal axis of the UV map) at that point on the surface. This means the
tangent direction rotates when you rotate a UV island. Two otherwise identical
meshes with differently oriented UVs will have different tangent directions at
the same geometric location.

**Binormal (B)**
The binormal (or bitangent) is the third axis, perpendicular to both the normal
and the tangent. It points along the surface in the remaining direction --
roughly corresponding to the V axis of the UV map (the "vertical" direction of
the UV layout).

The name "binormal" comes from differential geometry and is slightly imprecise
in this context. "Bitangent" is arguably more accurate. Both terms are used in
the industry -- you will see both in documentation and software. They mean the
same thing here.

> **TODO:** image -- a polygon with all three TBN vectors drawn as colored
> arrows: normal pointing out, tangent pointing along U, binormal pointing
> along V. Show a UV grid alongside to make the U/V relationship clear.


### How Tangent Space Is Calculated

Because the tangent direction depends on UVs, computing it requires looking at
both the geometry and the UV layout together. Several algorithms exist for
doing this.

**MikkT space** (Mikkelsen Tangent Space) is the de facto industry standard.
It was developed by Morten S. Mikkelsen and is used by virtually all modern
tools -- Blender, Marmoset Toolbag, Substance Painter/Designer, most game
engines, and most renderers. As long as both the tool that bakes a normal map
and the tool that renders it use the same MikkT implementation, the normal map
transfers correctly between them. When in doubt, use MikkT-compatible tools on
both ends.

**UV-based tangent calculation** (the general category MikkT falls into):
Tangents and binormals are computed from the UV coordinates of each face.
The tangent at a vertex is derived by looking at the UV coordinates of the
surrounding faces and finding the direction that corresponds to U increasing.
Because multiple faces share a vertex and each face may have slightly different
UV orientations, the final per-vertex tangent is averaged from the surrounding
faces (similar to how vertex normals are averaged from face normals).

**Implications for UV layout:**
Since tangents are derived from UVs, the quality of your UV layout directly
affects the quality of the tangent space -- and therefore the quality of any
normal maps baked onto the mesh. Highly distorted UVs produce inconsistent
tangent directions, which produces wavy, artifact-prone normal maps even if
the geometry is clean.


### The "Spin" Around the Normal

One way to think about the tangent: it is a vector that lies on the surface
plane and can point in any direction within that plane. Imagine a compass needle
lying flat on the surface -- it can spin freely around the normal as its axis.
The UV layout locks down which direction it points.

If you rotate a UV island by 90 degrees, the tangent at every vertex in that
island rotates 90 degrees around the normal. The geometry has not changed; only
the local tangent frame has rotated. This is why a normal map baked with one UV
orientation will look wrong if applied to the same geometry with a different UV
orientation -- the tangent space it was baked in no longer matches.


### Why This Matters for Modeling

The TBN frame is most famous for its role in normal mapping, but it is also
directly useful in modeling and sculpting workflows.

The three axes give you a local coordinate system relative to the surface at any
point. Many modeling tools let you move, push, or slide vertices along these
local axes:

- **Move along the normal** -- pushes or pulls the surface straight in or out,
  like inflating or deflating a balloon at that point. This is the basis of
  "move along normal" in sculpting and of inflate/deflate brushes. The surface
  grows or shrinks relative to its own facing direction, not relative to a fixed
  world axis.

- **Move along the tangent** -- slides the vertex sideways along the surface in
  one direction. The vertex stays on (or near) the surface plane and slides
  rather than lifting off it.

- **Move along the binormal** -- slides the vertex sideways along the surface in
  the other direction, perpendicular to the tangent.

The combination of tangent and binormal gives you two independent "sideways"
directions on the surface, both perpendicular to the normal. Together all three
axes let you navigate the surface in a way that is always relative to the
surface's own orientation -- useful when the model is at an unusual angle in the
world and you want to edit relative to the surface rather than relative to world
XYZ.

> **TODO:** image -- diagram showing the three TBN axes on a curved surface
> with arrows showing the direction of effect for each: N pushes in/out,
> T slides one way, B slides the other way.




---




Part 4 -- Types of Polygon Mesh Models
=======================================

Not all polygon meshes are used the same way. Understanding the different
categories of polygon mesh and how each is used in a pipeline shapes almost
every modeling decision you will make. See also [[Polygon-Meshes]] for a more
concise overview.


Base Meshes
------------

The base mesh is the primary working mesh -- the one you sculpt into, add UVs
to, assign materials to, mark hard and soft edges on, and deliver down the
pipeline. It is the authoritative version of the model.

For deformable models like characters, the base mesh is usually the mesh that
gets rigged and skinned -- the skeleton deforms the base mesh when joints move.
(Some pipelines rig a higher subdivision level, but this is less common.)

Base meshes are the source from which other versions of the mesh are derived:

- **Subdivision surfaces** -- the base mesh is subdivided to produce a smooth
  surface.
- **Multi-level subdiv** (ZBrush, Blender, etc.) -- multiple levels of
  subdivision are stored simultaneously; the base mesh is the lowest level.
- **Optimized-poly / "low-poly"** -- a polygon-reduced version optimized for
  real-time rendering.
- **Complex representations** (Nanite in Unreal Engine, etc.) -- a computed
  efficient representation derived from the base mesh.


Subdivision Surface Cage Models
---------------------------------

A subdivision surface cage (often just called a "subdiv cage" or "the cage") is
a polygon mesh that will be run through a subdivision algorithm to produce a
smooth surface.

The cage model itself looks blocky and angular -- that is intentional. The
subdivision algorithm adds new geometry and repositions existing vertices to
produce a smooth result. The artist models the cage, and the algorithm handles
the smoothing.

In multi-level subdivision workflows, the cage is the lowest subdivision level
-- level 1 in ZBrush, or subdivision iteration 0 in Blender, for example.

Subdivision surface models are the most common model type used for characters
and organic props in film CG production. The algorithm most commonly used is
Catmull-Clark subdivision, or some derivative of it (e.g., OpenSubdiv, which
is used in most modern film renderers).

See Part 7 for topology rules specific to subdivision cage modeling, and
[[Topology-for-Subdiv]] for the detailed reference.


Optimized-Poly / "Low-Poly" Models
------------------------------------

"Low-poly" is a historical term that now means different things in different
contexts. A clearer way to describe these models is **optimized-poly-count
models**: meshes where every polygon is justified and the count is kept to the
minimum that meets all other requirements.

The polygon counts on optimized-poly models might actually be very high by the
standards of a decade ago. "Low" is relative and has changed enormously as
hardware has improved. The key idea is not that the count is low, but that
the count is not padded with unnecessary geometry.

As of 2026, optimized-poly models are still the dominant model type used in
real-time game engines. Every polygon, edge, and vertex has a cost at runtime,
so keeping things tight matters.

See the "Justify Every Component" section below, and Part 7 on optimization.


Complex Representations
------------------------

Systems like Nanite (Unreal Engine) and similar micro-polygon / mesh-shader
approaches generate highly optimized runtime representations from a source
polygon mesh.

Even these complex representations ultimately render (mostly) triangles deep
inside the hardware pipeline -- they just do so via sophisticated intermediate
representations that manage LOD and visibility automatically, rather than relying
on the artist to maintain separate LOD versions.

These representations are derived from regular polygon source meshes, often
very high-poly ones. The typical workflow: model or scan as detailed as needed,
then let the system build its complex representation automatically.

> **TODO:** brief section on LOD (Level of Detail) as a separate but related
> concept -- hand-authored LOD chain vs. automated LOD systems.




---




Part 5 -- Justify Every Polygon Mesh Component
===============================================

*Every vertex, edge, and face needs a reason to exist.*

This principle applies to all types of polygon mesh work, but it is most
critical on optimized-poly models where every component has a direct runtime
cost.


Why Every Component Needs a Reason
------------------------------------

Extra mesh components that serve no purpose:

- Increase vertex counts (and therefore GPU memory and processing cost)
- Can cause unexpected shading artifacts
- Interfere with UV layouts
- Create problems for deformation and rigging
- Make the mesh harder for other artists to understand and work with

A component has a reason to exist if it serves any of the following:

- **Shape** -- it defines the silhouette or a surface detail
- **Deformation** -- it provides geometry needed for joints to bend cleanly
- **Topology flow** -- it is an edge loop needed for subdivision or animation
- **Vertex colors** -- it holds vertex color data required by the pipeline
- **UV mapping** -- it is needed to create a seam or boundary for the UV layout
- **Material boundaries** -- it separates regions with different material
  assignments
- **Hard/soft edges** -- it is a boundary needed for normal smoothing
- **Creases** -- it carries crease weighting data for subdivision surfaces
- **Bevel weights** -- it carries bevel weight data
- **Other pipeline data** -- it carries some other per-vertex or per-edge data
  required by a specific pipeline stage

If a component does not serve any of these purposes, remove it. (And yes --
"we don't have time to fix it" is sometimes the justification in production.
That is not ideal, but it is real.)


Vertex Splitting -- The Hidden Cost of Unnecessary Complexity
--------------------------------------------------------------

Vertex splitting is something that happens in most rendering engines and graphics
hardware, usually invisible to the artist because the engine handles it
automatically. But understanding it helps explain why certain kinds of mesh
complexity are more expensive than they appear.

In a 3D modeling tool, a vertex is a single point shared by multiple faces. But
in the final rendered representation, each vertex can only hold one copy of each
attribute -- one set of UV coordinates, one normal direction. When a vertex sits
on a UV seam, or at a hard edge, or at a corner where many edges meet, it needs
different attribute values on each side.

The solution is to **split** (duplicate) the vertex -- one copy for each unique
combination of attributes. The original mesh might have 1,000 vertices, but the
final rendered version might have 3,000 or more, after splitting.

This is why a sphere made of thousands of tiny flat-shaded facets is more
expensive to render than a sphere with the same polygon count using smooth
shading: every vertex on the flat-shaded sphere must be duplicated once per
connected face (because each face needs its own copy of the per-face normal).
The smooth sphere's vertices are each shared cleanly.

Most of the time artists don't interact with this directly. But it is the reason
"optimize your vertex count" matters even when your polygon count looks fine.

> **TODO:** image -- diagram showing a vertex split at a UV seam. Before:
> one vertex shared by two faces. After: two vertices, one per face, each
> with its own UV coordinate.




---




Part 6 -- Topology
==================

What Is Topology?
------------------

In 3D modeling, **topology** refers to the structure of a polygon mesh -- how
the vertices, edges, and faces are connected and arranged across the surface.
Topology is the "blueprint" of the mesh.

Two meshes can represent the same shape but have completely different topologies.
A sphere could be modeled as a UV sphere (rows and columns of quads, with poles
at top and bottom), as an icosphere (triangulated subdivisions of an icosahedron),
or as a subdivided cube. All are spheres, but their topologies are radically
different, and each has different strengths and weaknesses for different purposes.

Topology is invisible in a final render -- it does not directly appear in the
output image. But it profoundly affects:

- How the mesh deforms when animated
- How it looks when subdivided
- How clean the UV layout can be
- How the surface shades under lighting
- How efficiently it renders
- How easy it is to work with in future stages of the pipeline

See also:
- [[Edge-Flow-for-Polygon-Meshes]] -- a focused look at edge loops and edge
  flow; good to read before diving into topology guidelines
- [[Topology-For-Polygon-Meshes]] -- topology guidelines and rules for polygon
  mesh modeling


Why Good Topology Matters
--------------------------

> **TODO:** expand this section with artist-friendly explanations, using
> concrete examples of good vs. bad topology and their consequences. Perhaps
> side-by-side renders of a character joint with good topology vs. bad topology
> when bent.

- Good topology makes a mesh **deform predictably**. Bad topology makes it
  crumple, pinch, or stretch in unexpected ways during animation.
- Good topology makes a mesh **subdivide cleanly**. Bad topology causes
  pinching, wrinkling, and unwanted bumps.
- Good topology makes **UV unwrapping easier** and produces cleaner, less
  distorted UV layouts.
- Good topology makes the **shading correct**. Bad topology causes shading
  artifacts -- dark spots, bright spots, and strange gradients that have
  nothing to do with the lighting.
- Good topology makes a mesh **easier for other artists to understand and
  modify**. The structure tells a story about the surface's intent.


Edge Loops
-----------

An **edge loop** is a continuous path of edges that travels around the surface
of a mesh, with each edge connected to the next by a shared vertex. On a
quad-based mesh, an edge loop follows a predictable, unambiguous path. It can
wrap around an entire object (like a ring around a cylinder) or terminate at a
pole.

Edge loops are the primary structural element of polygon mesh topology. They:

- Define where detail lives on the surface
- Allow modelers to add or remove detail in controlled, predictable ways
- Determine how the mesh deforms when animated
- Control how subdivision algorithms subdivide the surface
- Provide the seams and boundaries for UV maps

> **TODO:** image -- a simple mesh (e.g., a cylinder or a limb) with an edge
> loop highlighted by color.


### Edge Flow

**Edge flow** refers to the direction and path that edge loops take across a
surface. Good edge flow means the edge loops follow the natural contours of the
shape -- like grain in wood, or the flow of muscles under skin.

Poor edge flow means edge loops run in directions that fight against the shape,
producing topology that is harder to work with, deforms badly, and often shades
poorly.

Edge flow becomes most important on organic shapes -- characters, creatures,
faces -- where the surface needs to move during animation. For hard-surface
models (machines, architecture, vehicles), edge flow is still relevant but the
rules are somewhat different.

> **TODO:** image -- character face with good edge loop flow shown. Classic
> example: concentric loops around the eyes and mouth, following the orbicularis
> muscle groups. Explain why this is correct.


Poles -- Valence and When to Use Them
---------------------------------------

**Valence** is the number of edges that meet at a vertex. On a pure quad mesh,
the ideal valence is 4. A vertex with valence 4 is sometimes called a "regular"
vertex. The vast majority of vertices on a well-constructed base mesh should
have valence 4.

A **pole** is a vertex with a valence other than 4.


### N-Poles (Three Edges, Valence 3)

An N-pole is a vertex where only three edges meet. The name comes from the shape
of the letter "N", which has a visual structure of three edges if you break it
down as: `| \ |`

N-poles are common and often necessary. Any time an edge loop terminates (rather
than wrapping all the way around), it terminates at an N-pole. They occur
naturally at corners and transitions.

N-poles cause some pinching in subdivision surfaces if placed in high-curvature
areas. Placing them on flat or low-curvature regions of the surface minimizes
their impact.


### E-Poles (Five Edges, Valence 5)

An E-pole is a vertex where five edges meet. The name comes from the shape of
the letter "E", which has five terminuses if you break it down as two short
vertical strokes and three horizontal strokes: `| |` and `- - -`

Like N-poles, E-poles are common and often unavoidable. They occur wherever one
edge loop terminates into another, which is necessary any time topology changes
density or direction. E-poles also cause some pinching in subdivision, which is
minimized by placing them on flat or low-curvature areas.

N-poles and E-poles often come as a pair: whenever you redirect or terminate an
edge loop, you typically create one N-pole and one E-pole, which together resolve
the topology change.


### High-Valence Poles (Valence 6 or More) -- Avoid

High-valence poles are vertices where six or more edges meet. These should be
avoided in almost all cases, and some studio pipelines have strict rules against
them.

High-valence poles create severe artifacts when the mesh is subdivided --
sometimes called "cat's ass" artifacts (a somewhat indelicate but memorable
description in the industry). The subdivision algorithm concentrates too much
geometry at the high-valence point and produces pinching, bunching, and visible
bumps on the smooth surface.

> **TODO:** image -- a mesh with a high-valence pole, and the subdivided result
> showing the artifacts. Use this as a "what not to do" example.

On the opposite end: a vertex with valence 2 is a degenerate case -- it is just
a point on a line with no surface area. These should never appear in a mesh
except on boundary edges of an open mesh, and even there they are usually
unintentional and a sign of a mesh problem.


### Valence Summary

| Valence | Name           | Notes                                                |
|---------|----------------|------------------------------------------------------|
| 3       | N-pole         | Common, often needed; avoid on high-curvature areas  |
| 4       | Regular vertex | Ideal; aim for this on most of the mesh              |
| 5       | E-pole         | Common, often needed; avoid on high-curvature areas  |
| 6+      | High-valence   | Avoid -- causes severe subdivision artifacts         |




---




Part 7 -- Topology for Specific Purposes
=========================================


Topology for Subdivision Surfaces
-----------------------------------


### What Subdivision Does

Subdivision surface algorithms take your polygon cage and add new geometry,
then reposition all the vertices (both old and new) to produce a smoother
surface. The most common algorithm is **Catmull-Clark subdivision**, or
derivatives of it such as **OpenSubdiv** (used in most modern film renderers
and game engines).

When people in the industry say "subdiv" without further qualification, they
almost always mean Catmull-Clark or a variant. Other subdivision algorithms
exist (Loop subdivision, PN triangles, etc.) but are rarely encountered in
standard 3D art pipelines.

Each iteration of subdivision (each "level") multiplies the polygon count by
four. A cage with 1,000 faces becomes 4,000 at level 1, 16,000 at level 2,
64,000 at level 3, and so on.

> **TODO:** image sequence -- the same cage at levels 0 (cage), 1, 2, 3.
> Show how each subdivision adds geometry and smooths the result.


### Stretching and Tension

We usually want the general flow and spacing of edges to change gradually across
the mesh -- spacing and direction should transition across several edge loops,
not abruptly all in one spot.

When there is too much difference in edge spacing or direction concentrated in
a small area, this creates **tension** in the subdivision surface. Tension shows
up as pinching, pulling, or uneven smoothing in the subdivided result. The mesh
looks like it has been stretched or compressed unevenly, even if the cage itself
looks reasonable.

The fix is to **resolve tension** by adjusting the surrounding vertices --
adding transitional geometry, spacing edges more gradually, or redirecting edge
loops so that the change happens over a larger area.

> **TODO:** image pairs -- (X marks) mesh with tension causing a bad subdivided
> result, and (checkmarks) the same area resolved, with the corresponding
> improved subdivided result.


### Rules for Subdiv-Friendly Topology

> **TODO:** detailed rules section. Cover the main requirements for clean
> Catmull-Clark subdivision: all-quad or mostly-quad cage; pole placement on
> flat areas; avoiding high-valence poles; support loops for sharp edges vs.
> crease weighting; specific topology patterns for common shapes (cylinder
> caps, elbow joints, spheres, etc.).

See [[Topology-for-Subdiv]] for the detailed reference.


Topology for Animation and Deformation
----------------------------------------


### Edge Loops Around Joints

The rule of thumb: edge loops should be **perpendicular to the axis of
bending**. A knee bends forward and back; the edge loops around it should be
horizontal rings encircling the leg. An elbow bends in a similar way. The loops
give the mesh "room" to compress on the inside of the bend and stretch on the
outside.

More edge loops near a joint = softer, more gradual deformation. Fewer loops =
sharper bending, which may look good for a robot but wrong for an organic
character.

> **TODO:** image -- a simple limb (arm or leg) with edge loops visible, bent
> at the joint. Show good topology with smooth deformation vs. insufficient
> loops with a sharp pinch.


### Facial Topology

Faces have some of the most demanding topology requirements of any part of a
character. The face must deform for a huge range of expressions -- smiles,
frowns, wide eyes, pursed lips, brow raises, cheek puffs -- and it must do so
without pinching, tearing, or looking wrong from any angle.

The traditional approach for organic facial topology is **concentric edge loops
around the primary expression muscles** -- the orbicularis oculi (around the
eye), the orbicularis oris (around the mouth), and the major cheek muscles.

> **TODO:** detailed facial topology section with diagrams. Classic reference
> material. Show the concentric loop structure, where loops cross and terminate,
> and why this pattern works for the underlying anatomy.


Topology for Hard-Surface Modeling
------------------------------------

Hard-surface models (machines, vehicles, weapons, architecture) have somewhat
different topology requirements than organic models. They often need sharp,
well-defined edges and flat panels, rather than the smooth flowing curves of
a character.


### Support Loops

When using subdivision surfaces on a hard-surface model, you need a way to
keep edges sharp. Subdivision naturally rounds everything out -- that is its
whole purpose. Support loops (also called holding edges or control loops) are
extra edge loops placed very close to an edge that you want to stay sharp.

The tighter the support loops are to the edge, the sharper the result after
subdivision. Very tight support loops produce near-90-degree edges. Loops
further away produce a soft, gradual bevel.

> **TODO:** image -- an edge with no support loops (rounds to nothing after
> subdiv) vs. the same edge with tight support loops (stays sharp). Show
> the cage and the subdivided result side by side.

The main downside of support loops: they add polygons everywhere. On a complex
model, managing support loops for every sharp edge can substantially increase
complexity.


### Hard Edge Loops

An alternative to support loops for many situations is simply marking the edge
as a hard edge (see Part 3). This avoids adding extra geometry for sharpness
and instead relies on normal-smoothing control.

Hard edge loops are efficient and can look great, but they look sharp at all
subdivision levels and distances -- they don't integrate as naturally with the
soft surrounding surface as geometry-based sharpness does.


### Crease Weighting

A third option, available in most modern subdiv implementations (including
OpenSubdiv), is **crease weighting**: assigning a numerical sharpness value
to edges. A crease weight of 0 is completely smooth (normal subdivision). A
crease weight of 1 is fully sharp (the edge doesn't move during subdivision).
Values between 0 and 1 give semi-sharp creases.

Crease weighting is a powerful alternative to support loops. It adds no extra
polygons, is easy to adjust, and integrates cleanly with the subdivision
algorithm.

> **TODO:** image comparison -- same edge with support loops vs. crease weight.
> Show the difference in cage complexity and in the subdivided result.


### Booleans

> **TODO:** section on using boolean operations in hard-surface modeling.
> Cover when they are useful, what problems they create (n-gons, bad topology),
> and how to clean up after them.


### Crease-to-Blended Transitions

> **TODO:** section on transitioning from a sharp crease to a smooth blended
> area of the surface. Common problem in hard-surface modeling. The four main
> approaches: edge spacing, edge loop termination, hard edges, and crease
> weights.


Topology for UV Mapping
-------------------------

UV mapping is the process of "unfolding" the 3D surface of a mesh into a flat
2D layout so that 2D textures can be applied to it. The topology of a mesh
directly affects how well it can be unwrapped.

> **TODO:** this section needs detailed development. Key topics to cover:
> - Edge loops as natural seam placement locations
> - Poles and how they affect UV distortion
> - N-gons and how they complicate unwrapping
> - The difference between UV seams and hard edges
> - "Island" structure and how topology determines what can be a clean island

See the UV mapping notes for full coverage.


Topology for Game Engines and Optimization
-------------------------------------------


### Polycount and Its Meaning

> **TODO:** explain polycount in practical terms for artists. Clarify the
> difference between face count and triangle count (which is what actually
> matters at the hardware level). Give rough guidelines for different
> platforms and use cases, noting that these change constantly as hardware
> improves.


### Level of Detail (LOD)

> **TODO:** explain LOD -- the practice of creating multiple versions of a
> mesh at different polygon counts, which the engine switches between based
> on camera distance. Cover the basic principles of how to plan LOD-friendly
> topology from the start.




---




Part 8 -- Modeling Approaches
==============================

Different modeling workflows start from different points and use different tools.
Understanding the main approaches -- and when each is appropriate -- is a big
part of learning to model efficiently.

> **TODO:** all subsections below need development. This part is skeleton only.


Box Modeling
-------------

Start from a primitive shape (cube, cylinder, sphere) and push, pull, subdivide,
and add geometry until you arrive at the final form. Box modeling is intuitive,
broadly applicable, and tends to produce good topology because you are always
working with the same underlying mesh.

Best for: most things. It is the most common general-purpose approach.


Poly Modeling
--------------

Start from a single polygon (or a small number of polygons) and extrude, extend,
and fill in the surface manually, polygon by polygon. Gives very tight control
over every part of the topology.

Best for: situations where you have very specific topology requirements and need
to place every edge loop deliberately.


Sculpting and Retopology
-------------------------

Sculpt a high-polygon model freely (in ZBrush, Blender, etc.) without worrying
about topology at all. Then "retopologize" by drawing clean, purpose-built
topology over the surface of the sculpt.

Retopology is common for characters and organic models: sculpt the form, then
build clean production topology over it, using the sculpt as a surface reference
and as a normal map source.

> **TODO:** explain the retopology workflow in more detail -- the tools used,
> the typical steps, and how the sculpt and the retopologized mesh are used
> together downstream.


Subdivision Surface Modeling
-----------------------------

Work at the cage level while keeping subdivided preview on. You model the
simple cage but see the smooth result in real time. This is the dominant
character modeling workflow in film production.

Requires understanding how changes to the cage propagate through the subdivision
algorithm. Covered in Parts 2 and 7.


Boolean Modeling
-----------------

Use boolean operations (union, subtract, intersect) to combine and cut primitive
shapes. Very fast for complex hard-surface shapes that would be tedious to model
by hand. The main downside is that booleans almost always produce messy topology
that needs cleanup.


Procedural and Parametric Modeling
------------------------------------

> **TODO:** brief section. Cover node-based modeling (Blender geometry nodes,
> Houdini), parametric CAD-derived workflows, and how these relate to
> traditional polygon modeling.




---




Part 9 -- Common Problems to Avoid
====================================

> **TODO:** each item below needs development with images. Each should become
> a full subsection explaining what the problem is, why it happens, why it
> matters, and how to fix or prevent it.


N-Gons and When They Are Actually OK
--------------------------------------

N-gons cause problems for subdivision, animation, and UV mapping. They should
generally be avoided. However, on flat, non-deforming, non-subdivided surfaces
where the n-gon can be clearly triangulated without issue, they are sometimes
acceptable -- particularly as an intermediate state during modeling, before
a final cleanup pass.

Rules of thumb:

- N-gons on flat hard-surface panels: often OK in practice
- N-gons on curved surfaces: avoid
- N-gons on any surface that will be subdivided: avoid
- N-gons on any surface that will deform during animation: avoid
- N-gons on a game engine mesh: usually avoid (triangulate unpredictably)

- In general, the trend is that temporary N-gons will often exist for convenience while working, which is fine, as they will be fixed in later stages. Most software has tools to easily find all the n-gons later so they can be cleaned up. Some software can even automatically clean them up.

> **TODO:** examples with images.


Non-Manifold Geometry
-----------------------

A **manifold mesh** is one that could physically exist as the surface of a
real-world object. Picture a solid object in front of you -- a coffee mug, a
rock, a machine part. Its surface is a closed, continuous shell. Every point
on that surface is surrounded by other surface on all sides, with no gaps, no
internal floating sheets, no places where the surface folds back through itself,
and no paper-thin knife edges where two sheets meet at a single line. That
is manifold geometry.

If you look at a mesh and can imagine it being 3D-printed or cast in metal --
if it reads as the surface of a believable volume -- it is probably manifold.
If you find geometry that would require physical matter to occupy the same space
as other matter, or a surface that is infinitely thin in a way that no real
material could be, that is probably a non-manifold condition.

More formally: a manifold mesh is one where every edge is shared by **exactly
two faces**, and the faces around every vertex form a single continuous fan with
no gaps or folds.


### Non-Manifold Edges

A **non-manifold edge** is one shared by the wrong number of faces:

- **Shared by three or more faces** -- a T-junction or interior sheet. Common
  after boolean operations. One edge cannot have three faces attached to it
  in a physically sensible way.

- **Shared by only one face and not on an open boundary** -- a dangling edge,
  or a fin. A single face with one free edge sticking out into space.

An open mesh (a surface with intentional holes or open borders, like a flat
plane) has boundary edges that are legitimately shared by only one face. That
is not a non-manifold condition -- it is an open boundary. The non-manifold
condition is specifically an edge that should be interior but is attached to
the wrong number of faces.

> **TODO:** image -- three examples side by side: (1) a normal interior edge
> shared by exactly two faces (good); (2) three faces sharing one edge (bad);
> (3) a single-face fin edge (bad).


### Non-Manifold Vertices

A **non-manifold vertex** is one where the surrounding geometry does not form
a single continuous fan of faces. The most common case is two separate surfaces
that share a single merged vertex but share no edge -- sometimes called a
**bowtie vertex** or **pinch vertex**.

Imagine two triangles touching at only one corner point. They share a vertex,
but they have no shared edge between them. In the mesh data, those two
triangles are technically "connected" -- they share an index -- but the
connection is infinitely thin. There is no surface area, no edge, no
meaningful physical connection, just a mathematical point they happen to
both reference.

This is always wrong. Faces that are meant to be stitched together should
share an **edge**, not only a vertex. A shared vertex with no shared edge
creates a topological pinch point that breaks subdivision, UV unwrapping,
and most other operations that need to traverse the mesh surface.

> **TODO:** image -- two triangles touching only at one vertex (bowtie), vs.
> the correct version where they share an edge. Make the "infinitely thin
> connection" idea visually obvious.


### Non-Manifold Normals (Inconsistent Winding)

A subtler class of problem: two faces that share an edge but have **opposing
normal directions** -- one face's normal points outward and the adjacent face's
normal points inward. They are sharing the same edge, so the edge count is
fine, but the faces are oriented inconsistently.

This creates a surface that is locally "inside-out" at the boundary -- the
renderer sees an outward-facing surface on one side of the edge and an inward-
facing surface on the other. Under backface culling, this produces visible
holes or dark seams along the affected edges. Under subdivision, it causes
the algorithm to produce incorrect results at the inconsistent boundary.

This is why "make consistent normals" / "unify normals" is such a commonly
used cleanup command. It traverses the mesh from face to face across shared
edges and flips any face whose winding order is inconsistent with its
neighbors, making all normals agree about which direction is "outward."

> **TODO:** image -- a mesh with two adjacent faces, one outward-facing
> (normal shown pointing out) and one inward-facing (normal shown pointing in),
> sharing an edge. Show the shading artifact this produces.


### Surfaces, Volumes, and Open vs. Closed Meshes

A polygon mesh is always a **surface** -- a thin shell with no inherent
thickness or interior. The mesh itself has no volume. It is two-dimensional
geometry embedded in three-dimensional space, like a sheet of paper crumpled
into a shape.

**Volume** is the three-dimensional region enclosed by a surface. A physical
coffee mug has volume; a polygon mesh modeled to look like that coffee mug
does not contain volume -- it only represents the boundary of the volume the
real object would occupy.

This distinction matters because many operations (booleans, 3D printing,
physics, voxelization) need to work with volumes, not just surfaces. To use a
polygon mesh as a stand-in for a volume, the mesh must meet certain conditions.


#### Open and Closed Meshes

A **closed mesh** (sometimes called a watertight mesh) has no boundary edges.
Every edge is shared by exactly two faces, and the surface forms a complete,
unbroken shell -- like the outside of a solid object. There are no holes, no
open borders, no places where the surface just stops.

An **open mesh** has one or more boundary edges -- edges shared by only one
face. This means there are gaps or holes in the surface. A flat plane is
open. A tube with both ends cut off is open. A character's eyeball socket is
open. A coin modeled as just the top and bottom faces with no sides connecting
them is open.

Open meshes are valid and common. Many models are intentionally open -- objects
that are never seen from the inside do not need a closed shell. But an open
mesh cannot represent a volume, because its surface does not fully enclose any
region of space.

> **TODO:** image -- a closed mesh (e.g., a sphere -- completely sealed) next
> to an open mesh (e.g., the same sphere with a hole cut in it). Label the
> boundary edges of the open mesh.


#### When a Mesh Cleanly Represents a Volume

Four conditions together are what allow a polygon mesh to unambiguously
represent a volume:

1. **Closed** -- no boundary edges; the surface completely encloses a region.
2. **Manifold** -- every edge shared by exactly two faces; no bowtie vertices.
3. **No self-intersections** -- the surface does not fold back through itself.
4. **Consistent outward-facing normals** -- all face normals point away from
   the enclosed volume, so the mesh has a clear "outside" and "inside."

When all four conditions are met, any point in 3D space falls unambiguously
on one side or the other of the surface. The mesh defines a clear **inside**
and a clear **outside**. You can ask "is this point inside the object?" and
get a reliable answer.

This property is what makes so many operations possible:

- **Booleans** (union, subtract, intersect) work by determining which parts
  of each mesh are inside the other, then combining or discarding those
  regions. Without a reliable inside/outside, the operation is undefined.

- **3D printing slicers** need to know which regions to fill with material.
  A mesh that doesn't cleanly enclose a volume cannot be sliced correctly.

- **Signed distance fields (SDFs)** represent the distance from any point to
  the nearest surface, with positive values outside and negative values inside.
  This signed distinction only exists when the mesh has a clear inside and
  outside.

- **Voxelization and DynaMesh-style operations** (ZBrush, Blender Voxel
  Remesh, etc.) fill the inside of the mesh with volume and rebuild the
  surface from scratch. They rely entirely on the mesh correctly defining
  where "inside" is.

Self-intersection is worth calling out specifically: even a closed manifold
mesh with consistent normals can fail the inside/outside test if the surface
crosses through itself. A figure-eight shape, for example, creates regions
where a ray cast from outside to inside crosses the surface an odd number of
times in some directions and an even number in others, giving contradictory
inside/outside answers. Any meaningful volume operation on a self-intersecting
mesh will produce incorrect results.

> **TODO:** image -- a closed manifold mesh with consistent outward normals
> (e.g., a sphere), with arrows indicating "outside" and "inside." Alongside
> it, a self-intersecting mesh to illustrate why self-intersection breaks
> the inside/outside test.


### Why Manifold Geometry Matters

Manifold geometry is important not as a rule for its own sake, but because a
huge number of downstream operations assume the mesh is manifold and produce
wrong or broken results when it is not.

**Subdivision surfaces**: Catmull-Clark and similar algorithms are defined
mathematically for manifold meshes. Non-manifold edges and vertices are
undefined cases -- the algorithm does not know what to do with them. The
result is usually garbage geometry at the non-manifold location.

**UV unwrapping**: unwrapping algorithms need to traverse the mesh surface
from face to face across edges. Non-manifold edges create ambiguity (which
side do you unwrap onto?), and non-manifold vertices create pinch points that
the unwrapper cannot correctly cut or flatten.

**Rendering and shading**: non-manifold geometry produces incorrect normals,
shading seams, and visible artifacts. Backface culling in particular behaves
unpredictably when faces are inconsistently wound.

**Physics simulation**: cloth, rigid body, fluid, and collision systems almost
all assume manifold surfaces. Non-manifold input produces incorrect collision
detection and simulation instability.

**Boolean operations**: booleans (union, subtract, intersect) require clean
manifold input. Non-manifold meshes produce incorrect or failed boolean results.

**Volume representations**: a closed manifold mesh is the surface of a
well-defined volume. This means it can be reliably converted to and from other
volume representations -- voxel grids, signed distance fields (SDFs), implicit
surfaces, and similar. This conversion is what makes 3D printing work (slicers
require manifold geometry), what makes volumetric booleans reliable, and what
allows tools like ZBrush's DynaMesh to convert your mesh into a volume and
back in order to merge separate elements together. A non-manifold or open mesh
cannot be used as a volume boundary because it is ambiguous where "inside" and
"outside" are.

**Common causes of non-manifold geometry**: boolean operations (especially
when the input meshes intersect or just touch), extruding faces but not
merging the boundary vertices, merging meshes without welding shared edges,
accidental duplication of geometry, and importing from CAD tools that
represent geometry differently.

Most modeling software has a "select non-manifold" command that finds and
highlights all non-manifold edges and vertices in one step. Run it as part of
any final mesh cleanup pass.

> **TODO:** images showing each type of non-manifold geometry.


Double Faces and Lamina Faces
-------------------------------

**Double faces** are two or more faces occupying the same space. They usually
result from accidental duplication. They look fine in the viewport but cause
shading artifacts on render and break most operations that analyze the mesh.

**Lamina faces** are faces that share all of their edges with another face but
have reversed normals -- effectively the same face front and back in the same
place.

Both are detected and removed by the "clean up" or "merge by distance" tools in
most modeling software.


Zero-Length Edges and Zero-Area Faces
----------------------------------------

> **TODO:** explain degenerate geometry -- edges with no length, faces with no
> area. How they arise (usually from collapsing or merging operations), why
> they cause problems, and how to find and remove them.


High-Valence Poles
--------------------

Covered in Part 6. Short reminder: valence-6-and-above poles cause severe
subdivision artifacts. Find and fix them using the "select all by type" tools
available in most modeling software.


Inverted and Inconsistent Normals
-----------------------------------

Covered in Part 3. Short reminder: use "check / make consistent normals" and
visually verify normals on any mesh before export or delivery.




---




Appendix -- Reference Tables
=============================


Polygon Type Quick Reference
------------------------------

| Type    | Sides | Use?     | Notes                                          |
|---------|-------|----------|------------------------------------------------|
| Tri     | 3     | Sometimes | Fine for game meshes; avoid for subdiv/anim   |
| Quad    | 4     | Yes      | Default choice for almost everything           |
| N-gon   | 5+    | Rarely   | Specific situations only; see Part 9           |


Valence Quick Reference
------------------------

| Valence | Name         | Notes                                               |
|---------|--------------|-----------------------------------------------------|
| 3       | N-pole       | Acceptable; keep off high-curvature areas            |
| 4       | Regular      | Ideal; aim for this on most verts                    |
| 5       | E-pole       | Acceptable; keep off high-curvature areas            |
| 6+      | High-valence | Avoid -- severe subdivision artifacts                |


Mesh Type Quick Reference
--------------------------

| Mesh Type             | Primary Use           | Main Topology Priority             |
|-----------------------|-----------------------|------------------------------------|
| Base mesh             | Working master mesh   | Clean, intentional, no waste       |
| Subdiv cage           | Film / organic        | All-quad, pole placement, tension  |
| Optimized-poly        | Game engines          | Min count, every component justified |
| Complex representation | Nanite, etc.         | Source mesh quality; auto-derived  |


---




Technical Details -- How Mesh Data Is Stored
=============================================

This section covers how the components described in Part 1 are actually
represented as data. It is more technical than the rest of this article and
is intended for readers who want to understand what is happening under the
hood -- either out of curiosity, or because they are working with mesh data
directly (scripting, pipeline tools, game engine internals, etc.).

Understanding even the basics here can sharpen your intuition as an artist.
When you know that a face is literally just a list of numbers pointing to
vertices, and that an edge is just two of those same numbers, it becomes much
easier to reason about why certain operations are fast or slow, why certain
problems arise, and how the data you assign to components (UVs, normals,
materials) is being stored and used.


How Vertices Are Defined
-------------------------

At the absolute minimum, a vertex is three numbers: its X, Y, and Z coordinates.

The simplest way to store all the vertices of a mesh is a **flat array** -- a
single sequence of numbers where every three values define one vertex:

```
x0, y0, z0,  x1, y1, z1,  x2, y2, z2,  ...
```

After every third number, one vertex is complete, and the next three numbers
implicitly define the next vertex. This format is extremely compact and is
what GPUs work with directly (it maps directly to a vertex buffer in OpenGL,
DirectX, Vulkan, Metal, and similar APIs).

Alternatively, the same data can be represented as a **list of tuples** --
one tuple per vertex, each holding three values:

```python
verts = [
    (x0, y0, z0),
    (x1, y1, z1),
    (x2, y2, z2),
    ...
]
```

Both formats contain the same information. The flat array is more memory-
efficient and GPU-friendly; the list of tuples is more readable and easier
to work with in code.

Either way, the order of the list matters. Each vertex has an **index** --
its position in the list, starting from zero:

```
verts[0]  is the first vertex
verts[1]  is the second vertex
verts[2]  is the third vertex
... and so on
```

These index numbers are how everything else in the mesh refers to vertices.
Once a vertex has an index, you never need to repeat its coordinates -- you
just reference the index number. This is called an **indexed mesh** or
**indexed face set (IFS)**, and it is the dominant representation in both
real-time and offline rendering.

The practical benefit: if you want to move a vertex, you change its three
numbers in the vertex array, and every face or edge that references that index
automatically reflects the change -- you do not have to update anything else.


How Faces Are Defined
----------------------

Once vertices have index numbers, faces are straightforward: a face is just
a **list of vertex indices**, one per corner.

A triangle has three corners, so it is defined by three indices:

```
face = [0, 1, 2]     ← a triangle using vertices 0, 1, and 2
```

A quad has four corners:

```
face = [0, 1, 2, 3]  ← a quad using vertices 0, 1, 2, and 3
```

An n-gon with five sides:

```
face = [0, 1, 2, 3, 4]
```

All the faces together form a **face list** (or **index buffer**):

```python
faces = [
    [0, 1, 2],
    [1, 2, 3],
    [3, 4, 5],
    ...
]
```

In the simplest case -- where every face is a triangle -- this can itself be
flattened to a single array, and once again the grouping is inferred:

```
0, 1, 2,  1, 2, 3,  3, 4, 5,  ...
```

Every three indices define one triangle. This flat triangle index array is
exactly what OpenGL, DirectX, Vulkan, and Metal accept as draw calls for
indexed geometry.


### Winding Order and Face Normals

The **order** in which vertex indices are listed matters. Two faces using the
same three vertices but listed in opposite orders are facing opposite directions:

```
[0, 1, 2]   ← vertices listed counterclockwise from the front → normal points toward you
[0, 2, 1]   ← vertices listed clockwise from the front → normal points away from you
```

This is the winding order, and it is how the renderer determines the face
normal direction. Consistent winding order across all faces of a mesh is what
produces consistent outward-pointing normals. This is why "flip normals" tools
exist -- they reverse the winding order of selected faces.


### N-Gon Triangulation -- Technical Notes

An n-gon with n sides always produces exactly **n - 2 triangles** when
triangulated, regardless of method. A pentagon gives 3 triangles, a hexagon
gives 4, and so on. The question is not how many triangles result, but whether
the triangles are valid -- non-overlapping, non-self-intersecting, and covering
the polygon's area cleanly.


#### Convex N-Gons -- Triangle Fan

A convex polygon (all interior angles less than 180 degrees) can be
triangulated by a simple **triangle fan**: pick any one vertex, then connect
it to every non-adjacent vertex with a diagonal. This divides the polygon into
n - 2 triangles fanning out from that one vertex. Any vertex can be the fan
center; all produce valid results.

The fan approach is fast, simple, and always works for convex polygons. It is
the method of choice when a polygon is known to be convex.

```
Pentagon fan from vertex 0:
  Triangle [0, 1, 2]
  Triangle [0, 2, 3]
  Triangle [0, 3, 4]
```

> **TODO:** image -- a convex pentagon with a triangle fan drawn in, showing
> the three resulting triangles.


#### Non-Convex (Concave) N-Gons -- Where the Fan Fails

A concave polygon has at least one interior angle greater than 180 degrees
(a "reflex" vertex -- one that points inward). At a reflex vertex, a
triangle fan from the wrong starting vertex will produce diagonals that pass
outside the polygon's boundary, and the resulting triangles will overlap or
self-intersect.

The standard algorithm for correctly triangulating any simple (non-self-
intersecting) planar polygon is **ear clipping**:

1. Identify all "ear" vertices -- vertices where the triangle formed with the
   two neighboring vertices lies entirely inside the polygon.
2. Clip (remove) one ear, outputting its triangle.
3. The remaining polygon has one fewer vertex. Repeat until only a triangle
   remains.

Every simple polygon with at least four vertices is guaranteed to have at least
two ears, so the algorithm always terminates successfully. It runs in O(n²)
time in a basic implementation, which is fast enough for any polygon count
you would encounter in a mesh.

The result is still n - 2 triangles, but the specific triangles produced
depend on which ears are found and in which order -- the output can look quite
different from a fan. The quality of the triangulation (how well-shaped the
triangles are) varies.

> **TODO:** image -- a concave polygon (L-shape or star notch), showing
> where a naive fan from one vertex would self-intersect, and alongside it
> the correct ear-clipped triangulation.


#### Non-Planar N-Gons -- The Hardest Case

The methods above assume the polygon is flat -- all its vertices lie in a
single plane (or close enough to one that projection is harmless). Non-planar
n-gons, whose vertices are spread across 3D space with no single flat plane
containing them, introduce a fundamentally harder problem.

The standard approach for non-planar polygons is **project, triangulate, lift**:
find the best-fit plane for the polygon's vertices, project them onto that
plane, run ear clipping in 2D, then lift the resulting triangles back to their
original 3D positions. This works acceptably when the polygon is only slightly
non-planar.

When a polygon is significantly non-planar -- vertices pulled far out of plane
-- the projected triangulation may produce triangles that, when lifted back to
3D, overlap or intersect each other. There is no clean 2D triangulation that
maps back to a correct 3D one. In the extreme case, determining whether a
non-planar 3D polygon even has a valid non-intersecting triangulation is an
NP-hard problem.

The visible result: non-planar n-gons that are naively triangulated often
produce crumpled, puckered, or visually wrong shapes at the triangulated area.
The triangles may fold back through each other or create abrupt shading breaks
that make no sense given the surrounding geometry. This is one of the most
common sources of unexpected-looking mesh problems when importing files between
applications.


#### The Quadrangulate-First Strategy

The cleanest approach to n-gon triangulation is to avoid dealing with n-gons
at the triangulation step entirely -- by converting them to quads (and possibly
one tri) beforehand. This is called **quadrangulation**.

The idea: rather than triangulating an n-gon directly, first decompose it into
a set of quads by inserting edges inside the polygon. Ideally most or all of the
quads are regular four-sided quads, with at most one tri left over if the vertex
count is odd. Then the entire mesh -- original quads and newly created quads
alike -- can be triangulated uniformly in one pass, with the same per-quad rules
applied consistently everywhere.

The advantages:
- The quads produced by quadrangulation are planar by definition (or much closer
  to planar than the original n-gon).
- The quad triangulation rules are well understood and predictable.
- The result integrates naturally with the rest of the mesh's quad topology.
- Triangle count is minimal (quadrangulation then triangulation still gives
  n - 2 triangles, same as direct triangulation).

Most tools that convert meshes to all-triangles (game engine importers, render-
time triangulation, cleanup scripts) apply some form of this strategy. They
first try to break n-gons into quads by adding well-placed edges, then handle
any remaining tris, and finally triangulate the whole mesh.

This is one of the main practical reasons why production assets avoid n-gons:
artists applying the quadrangulate-first strategy by hand -- dividing n-gons
into quads and tris during modeling -- produce predictable, clean results.
Assets that arrive at the triangulation step with n-gons still in them force
the software to make automatic decisions that may produce unintended, and
often incorrect-looking, geometry.


How Edges Are Defined
----------------------

Edges can be **implicit** or **explicit**, and each approach has different
trade-offs.


### Implicit Edges

If you have a face `[0, 1, 2]`, its three edges are completely implied:
vertex 0-to-1, vertex 1-to-2, and vertex 2-to-0. You do not need to store
edges separately -- they are inferred from the face list.

Simple index-list mesh formats work this way. The advantage is minimal data
-- only the vertex array and the face index array are needed. The disadvantage
is that certain queries are slow: "find all faces adjacent to edge 0-1" requires
scanning the entire face list, because edges are not stored explicitly as their
own entries.

This is fine for rendering (GPUs do not need topology queries; they just draw
triangles), but it is limiting for interactive mesh editing.


### Explicit Edges

Edges can also be stored as their own list, each defined as a pair of vertex
indices:

```python
edges = [
    [0, 1],
    [1, 2],
    [2, 0],
    ...
]
```

Like vertices, each edge has an index (its position in the list). Faces can
then be defined by **edge indices** instead of vertex indices:

```
face = [edge_0, edge_1, edge_2]   ← a triangle defined by three edge references
```

This redundancy -- edges referenced from both vertices and faces -- makes
adjacency queries fast. "Which faces share this edge?" is now a direct lookup
rather than a search. This is the approach taken by editing-optimized data
structures like the **winged-edge** and **half-edge** representations, which
store full connectivity information so that traversal from any component to any
adjacent component is constant-time.

The trade-off: explicit edge data takes more memory and is more complex to
maintain when the mesh changes. GPU rendering pipelines don't use it -- they
work with simple flat vertex and index arrays. Editing tools (Blender, Maya,
3ds Max, CGAL, etc.) use more sophisticated structures internally to make
operations like edge loops, edge collapses, and subdivision fast.


Per-Component Data -- It's All Just Data
-----------------------------------------

The geometric definition of each component -- position for vertices, index lists
for faces, index pairs for edges -- is just the minimum. Components are
essentially containers, and any additional information can be attached to them.

Different applications track different sets of data per component. The mesh is
ultimately a kind of database, and the components are the rows. You can
conceptually think of each vertex as a row in a spreadsheet, with one column
for position, one for UV, one for normal, and so on.

Below are the most commonly stored attributes for each component type. Most
production meshes carry some combination of these.


### Per-Vertex Data

| Attribute         | Description                                                      |
|-------------------|------------------------------------------------------------------|
| Position (X, Y, Z) | Always present. The vertex's location in 3D space.              |
| Normal (X, Y, Z)  | The vertex normal direction, for shading calculations. May be implicit (computed) or explicit (stored). |
| UV coordinates    | Texture mapping coordinates. A mesh can have multiple UV channels. Technically stored per face-corner, not per vertex (see note below). |
| Vertex color (RGBA) | Per-vertex color data, used for baked lighting, vertex painting, masking, etc. |
| Bone weights      | In skinned meshes, which bones influence this vertex and how much. Usually stored as a list of (bone index, weight) pairs. |
| Other custom data | Anything the pipeline needs -- blend shape deltas, custom material parameters, simulation data, etc. |


### Per-Edge Data

| Attribute       | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| Hard / soft     | Whether normals are averaged across this edge (soft) or kept separate (hard). |
| Crease          | A 0--1 value controlling how sharp this edge stays after subdivision (0 = fully smooth, 1 = fully sharp). |
| UV seam         | A flag marking this edge as a boundary for UV unwrapping.           |
| Bevel weight    | A 0--1 value controlling how much the bevel modifier affects this edge. |


### Per-Face Data

| Attribute            | Description                                                    |
|----------------------|----------------------------------------------------------------|
| Material index       | Which material slot is assigned to this face.                  |
| Smooth / flat flag   | Whether this face uses smooth or flat shading. In some apps this is per-face; in others it is driven entirely by hard/soft edges. |
| Triangulation        | For quad and n-gon faces: which diagonal direction to use when triangulating. Stored explicitly when the intended triangulation is not the software default. |
| Normal flip          | Winding order reversal -- some formats store this as an explicit flag rather than reversing the index order. |


### A Note on Face Corners (Loops)

Some attributes that feel like vertex data are actually stored per **face
corner** -- one value per face-per-vertex, not one value per vertex. UV
coordinates are the most important example.

A vertex sitting on a UV seam has two different UV positions -- one for each
side of the seam. If UVs were truly per-vertex, a seam would be impossible to
represent. So UVs are stored at the face-corner level: each corner of each face
has its own UV value, independent of other faces that share the same vertex.

Blender calls face corners **loops** and exposes them explicitly. Most other
applications handle this invisibly by splitting vertices at seams and hard
edges (vertex splitting, covered in Part 5). The end result is the same --
one UV and one normal per corner -- but the approach to storing it differs.


### More Complex Data Structures

Everything described above is the foundation. Real applications go further:

- **Interleaved vertex data**: instead of separate arrays for position, normal,
  UV, and color, all attributes for one vertex are packed together in memory:
  `x, y, z, nx, ny, nz, u, v, r, g, b, a, ...` then the same for vertex 1,
  and so on. GPUs often prefer this layout for cache efficiency.

- **Multiple UV channels**: a mesh can have several independent sets of UV
  coordinates (channel 0 for the main texture, channel 1 for lightmap UVs,
  channel 2 for detail textures, etc.).

- **Morph targets / blend shapes**: additional sets of vertex positions stored
  alongside the base positions. Each morph target is a full or partial set of
  positions that can be blended with the base mesh to create facial animation,
  corrective shapes, and similar effects.

- **Half-edge and winged-edge structures**: data structures used internally by
  editing tools that store full adjacency information -- each edge knows its two
  faces, each face knows its edges, each vertex knows its surrounding edges.
  These allow constant-time traversal of the mesh topology. They are invisible
  to artists but underlie most of what makes interactive editing fast.


### Stored vs. Derived Data

Not all of the data described above needs to be stored on disk or in memory.
A lot of it can be **calculated on demand** from other data that is already
present. Whether any given piece of data is stored explicitly or derived
implicitly is a design decision, and different applications and file formats
make different trade-offs.

Some examples:

**Tangents and binormals** are almost never stored on disk. They are derived
at runtime (or at import/load time) from the combination of vertex normals and
UV coordinates. The calculation is fast enough that there is rarely a reason
to pay the storage cost of keeping them on disk. MikkT-space tangents, for
example, are recomputed by the renderer or game engine from the mesh's normals
and UVs each time the asset is loaded.

**Normals** may or may not be stored, depending on whether the default
recalculated normals are acceptable. If a mesh uses standard smooth normals
with no custom tweaks -- no locked normals, no manually adjusted directions --
then the normals can simply be recomputed from the geometry and hard/soft edge
assignments every time the file is loaded. There is no need to store them.
When custom (explicit) normals are used, those values must be stored, because
they cannot be derived from geometry alone.

**Edges** (as described above) are often entirely implicit -- derived from the
face index list, not stored as their own data. Many file formats do not store
edge data at all, relying on the application to reconstruct it from the faces
on import.

**Edge attributes** like hard/soft assignments may be stored explicitly, or
they may be stored indirectly -- for example, as a smoothing angle threshold
value from which the hard/soft state of every edge is derived at load time.

The general trade-off is:

- **Storing data explicitly** saves calculation time at runtime but costs
  disk space and memory. It also means the stored values can drift out of
  sync if the geometry changes and the derived data is not regenerated.

- **Deriving data implicitly** saves disk space and avoids staleness, but
  costs calculation time every time the data is needed. If the derivation
  is expensive (or if the source data it depends on is not always available),
  this can be a problem.

Most applications store the minimum set of data needed to reconstruct everything
else, and recalculate derived values at load time or on demand. What that
minimum set is varies: a game engine optimized for fast loading might store
pre-baked tangents and normals to skip recalculation entirely; a 3D modeling
tool optimized for flexible editing might store only geometry and hard/soft edge
flags and derive everything else on the fly.




---


*Sources consulted for this article:*

- [GarageFarm -- Understanding Topology in 3D Modeling](https://garagefarm.net/blog/understanding-topology-in-3d-modeling)
- [Ebal Studios -- Polygon Modeling Practical Basics](https://www.ebalstudios.com/blog/polygon-modeling-basics)
- [TopologyGuides.com Encyclopedia](https://topologyguides.com/encyclopedia/)
- [Ikarus3D -- A Comprehensive Guide to Polygonal Modeling](https://ikarus3d.com/media/3d-blog/a-comprehensive-guide-to-polygonal-modeling/)
- [[Polygon-Meshes]] (T33D notes)
- [[Topology-for-Subdiv]] (T33D notes)
- [[Understanding-3D-Computer-Graphics]] (T33D notes -- Joe Crawford)

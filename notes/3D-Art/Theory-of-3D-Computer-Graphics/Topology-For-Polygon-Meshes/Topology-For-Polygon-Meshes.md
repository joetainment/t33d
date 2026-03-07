Topology Guidelines For Polygon Meshes
===============================

This document deals with how to give polygons best possible topology, meaning the best layout of polygons and edge loops to support a models shapes, and other goals.

This document assumes the reader has a good understanding of the basic theory behind polygon modeling. If not, reader's may wish to see [[Polygon-Mesh-Modeling-Theory]] for pre-requisite material.


Guidelines May be Strict or Soft
======================================

Depending on the project, work environment, etc, some of these guidelines might be considered absolute rules, whereas in other cases, they may be rough guidelines that need not be met in any exact way.

You should research your project's particular guidelines and requirements. If you are in charge of that for your project, and you don't have such guidelines and rules yet, then you should decide on some!



There Is No Perfect Answer For Complex Shapes
==============================================

Deciding on the best topology for complex models involves a lot of compromises and trade offs.

You can find a lot of long discussions online about what topology is the best. In fact, you will find many arguments this topic, often approaching the level of flamewars or religious arguments.

In reality, different situations are handled best with different topology guidelines, and in many cases, which topology is best is highly subjective, or specific to the particular nature of the project, the work, and the people involved.

From a technical sense, it should be noted that perfectly achieving our goals is often mathematically impossible. Ideally, in most cases, we'd want square quads of the same size across curved surfaces with no n-poles, or e-poles at verts.

Such a task *absolutely impossible*.  Instead, we just get the closest approximation that fits as many of our goals as best it can. This is similar to uv mapping, and many other situations in 3D computer graphics, then ideal goal is impossible, so we make compromises to get the best fit we can. (In fact, the difficulties and constraints faced are similar to those found in entirely different fields, such as defining "produceable surfaces" in physical real world manufacturing.)




Making The Right Decisions
==============================

The most important thing about topology is that *it is well reasoned*.
The topology isn't just random, it is laid out the way it is because that meets the needs of the models use, or meets the conventions/requirements established for a project.

So, when deciding on and determining topology for your models, always ask yourself...

*why*







Topology Guidelines - General
================================

- support shape    edges along what would be considered edge like sections in real-life  (parts where surface curvature is really strong/tight, where it can be considered a rounded edge even if it isn't an edge, strictly speaking)

- support easy manipulation by the artist. It's really hard to work with objects that have bad edge flow. Being able to select edge loops, edge rings, and clean paths or boundaries of edges along models is really helpful for artists to select components and manipulate them. Bad edge flow can waste so much artist time that in many situations its worth creating good edge flow topology just so it can be worked on more easily in the moment (see more detailed in section about edge loops in detail)

- support uv seams    sometimes edges and edge loops exists specifically because they defined an important place for a uv seam, even when those edge loops may otherwise not be needed

- support other data, such as vertex colors, material boundaries, creases, hard/soft edges, etc. 

- support deformation, especially for shapes that will be animated deforming, such as the legs of a character that will bend when walking.




Topology Guidelines - Optimized Meshes ("low poly" meshes)
================================


In addition to the more general guidelines above, optimized models should usually follow these guidelines.

Keep in mind that which guidelines are best for optimized meshs is especially project/game-engine dependent. Still, the guidelines below are widely applicable.


- Model should be all quads and tris prior to automated triangulation in the pipeline.

- Any triangulation that matters should be done explicitly on the artist-working model.

- Quads left untriangulated should generally be acceptable with either triangulation.

- Giant polygons should usually be cut up unless they will always be far away from the viewer.
     some game engines have issues with large polygons, one example being the fact that polygons are often culled, and a polygon that is even slightly on screen can't be culled, but if it is cut into multiple polygons, then some of those polygons could be.



Topology Guidelines - For Complex Representations of Polygons
================================================

Because there are so many potential types of complex representations of polygon meshes, (e.g. Unreal Nanite) it's impossible to come up with solid guidelines for these. However, since most complex representation end up being totally different from the input geometry, the exact topology of the input used to generate the complex representation doesn't matter. In fact system like Unreal's Nanite have often been designed to work well even with extremely messy topology, such as entirely triangulated meshes.




Topology Guidelines - Base Meshes For Subdivision Models
=============================================

In additional to the general guidelines, which still apply to subdivision models, subdivison models often have to take additions considerations into account.

- few or no tris
- few or no ngons
- no ngons of more than 5 sides
    
        Note that the first three, above, in the strictest scenario, amount to the model being "all quads", which very often is a strict requirement for assets in studio pipelines.

- quads are vaguely square-ish, not super distorted

- quads are of similar size (especially for multi level subdivision editing, such as sculpting high detail in ZBrush. If polygons arent of similar size, then in order to sculpt enough detail into the larger polygons, then smallest polygons end up being subdivided way too much, wasting huge amount of memory/storage and just generally slowing the computer down)

- faces and their edges have "low tension"  e.g. sections where it goes from larger to smaller polygons should happen gradually. sections that require a quad to be extrmely stretched rather than squarish can be made less extreme by adjust all the other polys around to accomodate it, so that all the stretching isn't all in one spot. generally we want the topology ot seem "relaxed". Software often even have on surface relax tools, which spread out the stretching of polys more evenly, while attempting to preserver the shape of the surface as much as possible.

- enough polygons, but not too many as to be a waste

    Base Meshes should have enough polygons, to visually represent the spirit of the intended shape and to provide enough detail for uvs, deformation, vertex colors, etc.

	Use more polys on the base mesh especially when it is:
		Bigger on screen (large or close up)
		Important "Hero" asset
		Will be intricately detailed
		Needing complex UV, Deformation, or other data on it's components
	
        (see more detailed section about this for more into)








How Much is Enough Polygons For Base Meshes? (detailed section)
==================================================================

    Base Meshes should have enough polygons, to visually represent the spirit of the intended shape and to provide enough detail for uvs, deformation, vertex colors, etc.

	Use more polys on the base mesh especially when it is:
		Bigger on screen (large or close up)
		Important "Hero" asset
		Will be intricately detailed
		Needing complex UV, Deformation, or other data on it's components

	How many polys the base mesh should have tends to depend on how important the object is, how big it is, how far away it is, and how detailed it will ultimately be.

	When you toggle the subdivision on or off, the overall shape of the object shouldn't really change much, it should just get a little rounder, (and possibly more detailed if multi subdivision level sculpting exists for it).

	An object before subdivision should, in spirit, look the same as the subdivided one except for being a little more jagged, since it doesn't have enough edges to appear round.
	The base mesh may also look significantly less detailed than the final subdivided one (if the model has multi-subdivision level sculpting stored for higher subdivision levels, or if displacement maps are being used on the high subdiv model).

	If the object changes too much, it's an indication that the poly count of the base mesh is too low.  In such cases, the base meshes should be given more geo, possibly even by subdividing the actual geo, and then making that subdivided mesh the base mesh and directly editing it's topology. Often in the early stages of modeling, artists will use subdivision on the actual model, but then "commit" that subdivision, making the actual editable base mesh itself have many more polygons. 

	A as quick rules of thumb:
	don't use cube that will be smoothed to represent spheres
	(unless it's for super tiny or far away object and 

	instead, use a slightly blocky/jagged spherical base-mesh, such as a cube that's been subdivided then spherified (verts projected to surface of imaginary sphere). This makes for a much better base mesh.

	remember that we need enough polys on the base mesh to support things like uvs, deformation, etc, so just because our base mesh looks rounder and the right shape at higher subdivision levels, that doesn't mean we have enough polys on the base mesh






Edge Loops In Detail
==========================

Good Edge Loops

clean edge loops that go all the way around the model and reconnect back where they started

A huge problem is spiral edge loops, that go around the model but don't reconnect with themselves when they make it back around the model, but instead continue around and around again, going up and down the model. Only in rare cases is this reasonable, such as on an actual metal screw, which does in fact have a spiraling edge. In most cases, spiraling edge loops makes things more difficult and should be avoided.


Ideally edge loops go around the model, but in many cases, they may need to merge, or converge into other edge loops. Such as when on side of the model has more polys that the other side.


Choosing whether to have edge loops the run all the way around without merging or converging, vs having evenly spaced and sized polygon, is a situation where conflicting goals means that a compromise must be reached and different trade offs considered. Generally, as long as the difference in polygon sizes is acceptable, we will have edge loops that go all the way around


[[image of hour glass like shapes, 2 cylinders with different radii along their lengths, on cylinder_a, the difference in radius of edge loops in minimal, meaning that the edge loops can go all the way around, no need for convergence/divergence or poles.  On the other the difference in radius at different points along the length is extreme, so in order to have similarly sized polys across the model, we can't have simple edge loops, and we have to have convergence/divergence/poles so that we can have different numbers of edge loops in different places, in order to keep the polys reasonably similar in size.]]

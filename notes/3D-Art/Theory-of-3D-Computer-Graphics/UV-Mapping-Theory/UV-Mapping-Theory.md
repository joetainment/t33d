UV Mapping Theory
==================

A four-part series on UV mapping theory by Joe Crawford of Teaching3D.
Covers UV coordinates from first principles through to practical workflow tips.

Original articles: [http://www.teaching3d.com](http://www.teaching3d.com)


---


Parts
------

- [[UV-Mapping-Theory--Part-1]] -- what UV coordinates are, normalization,
  tiling, utility textures
- [[UV-Mapping-Theory--Part-2]] -- UV sets, overlap, seams, islands,
  stretching, UV padding, projection mapping methods
- [[UV-Mapping-Theory--Part-3]] -- pelt/LSCM mapping, cutting and sewing UVs,
  layouts, UV snapshots, texture resolutions, workflow tips
- [[UV-Mapping-Theory--Part-4]] -- *(work in progress)* UV ranges, UDIMs,
  organizing textures into materials


---


Summary of Key Concepts
------------------------

**UV coordinates** assign each vertex a position in 2D texture space (the U
and V axes), determining how an image maps onto the surface of a 3D object.

**Normalization** means UV space always runs from 0 to 1 regardless of texture
resolution. Coordinates outside 0-1 tile the texture.

**Seams** are open edges in UV space -- boundaries where UV islands have been
cut apart to allow the mesh to unfold flat.

**Islands** are contiguous regions of the UV layout, analogous to elements
(shells) in 3D space.

**Stretching** occurs when polygon shapes in 3D space differ significantly from
their shapes in UV space.

**Pelt / LSCM mapping** is a modern approach where the artist marks seams and
the software automatically unfolds the mesh to minimize stretching.

**UV padding** is the space left between islands and texture edges to prevent
texture filtering from bleeding colors across borders.

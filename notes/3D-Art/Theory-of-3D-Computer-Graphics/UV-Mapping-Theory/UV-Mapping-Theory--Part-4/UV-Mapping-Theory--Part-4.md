UV Mapping Theory -- Part 4
============================

By Joe Crawford, founder of Teaching3D. Additional notes by T33D.
Original article: [http://www.teaching3d.com](http://www.teaching3d.com/)

*Continued from [[UV-Mapping-Theory--Part-3]]*

> **Note:** Parts of this document are unfinished and are a work in progress.


---


Good UVs Before Packing
------------------------

What we want from a UV layout before packing:

- **Square proportions** -- a square in the texture image should look square on
  the 3D object, not stretched into a long or wide rectangle.
- **Consistent texel density** -- the squares and numbers in a utility texture
  should be the same size everywhere. No tiny numbers on top and giant ones on
  the bottom.
- **Good orientation** -- numbers in a utility texture should be oriented in a
  way that makes sense. Usually pointing "up" so they are easy to read. Numbers
  should not be mirrored.
- **Minimal stretching and waviness.**
- **As few seams as possible.**

(There are exceptions and special cases.)


---


Organizing Textures
--------------------

The problem to be solved: how and where to place different objects onto different
textures so that the texture can be painted easily, and so it is efficient and
easy to work with for everyone else in the pipeline.

**Simple approach** -- each individual object has its own material. This is
often overly simple.

**Grouped approach** -- combine a bunch of objects that are logically part of a
group and would generally be seen at the same time. For example:

- The spaceship could all share one texture.
- The space pirate character could share another texture.

This method is used a lot in games. It is often not sufficient for film
productions.

**Strategy for UV layout and organizing textures into materials:**

- Come up with logical groupings of objects that can share textures and
  materials. Within a group, you make parts look different from each other by
  changing the texture rather than changing the material.
- For things that cannot be grouped together, put different materials on them.

**Example -- a gun:**

A gun could be all one material. The different parts of the gun can be laid out
in the UV editor and all fit into the 0.0 to 1.0 UV range (one single tile of
the texture). When painting in Photoshop, you can paint any part of the gun on
that single image.

**Example -- a room scene:**

Make a cube:
- Set width/height/depth to 64 units
- Set translateY to 32
- Flip the normals on the cube
- Turn on backface culling
- Delete the front face

This cube is now a "room." Add some boxes in one corner and some cylinders
(barrels) in another.

Now decide which materials you need:

```
polished_wood_floor_mat
    -- needs a diffuse texture for the wood
    -- if it's clean, reflection can probably just be set in the material

concrete_walls_mat
    -- for this, you need to lay out the walls onto a single texture
       so you can paint them
```


---



Texturing Per UV Range
=======================

As covered in Part 1, UV coordinates are normalized and tile continuously. The
"main" UV range is 0 to 1, but UV space extends in all directions -- 0 to 2, 2
to 3, negative values, and so on. So far we have treated all of this extended
space as just the texture repeating. That's the default behavior, but it is not
the only possibility.

The concept discussed in this section is: you can assign different image files
to different regions of UV space, so that the geometry sitting in one region
uses a different texture image from the geometry in an adjacent region.

This is a powerful idea that lets a single material cover a model with multiple
high-resolution textures at the same time -- without needing multiple materials.



How a Shader Can Do This
-------------------------

Nothing about this technique is technically unusual. A shader is just a program,
and it can do arbitrary math on UV coordinates before deciding which texture to
sample.

For example, a simple node setup could:

1. Read the UV coordinates.
2. Check: is the U value between 0 and 1? Or between 1 and 2?
3. Based on that, pass the UV into either TextureA or TextureB.
4. Output whichever texture was selected.

> *[Image needed: a simple shader node graph showing UV coordinates being split
> by a compare node, feeding into two different texture nodes, then merged --
> to illustrate the concept of choosing a texture based on UV range.]*

You could build this node network yourself and assign whatever textures and
ranges you like. There is no rule that says UV space has to be split into
regular 1x1 squares, or that there has to be any particular naming convention
for the files.

In practice though, handwriting this logic for every model would be tedious,
and texture-painting software would have no way of knowing where to put the
paint without a standard everyone agreed on. That is why systems like UDIMs
were developed.


---





UDIMs
------

**UDIM** is the standard for multi-tile UV workflows in film and high-end
production. The name comes from "U-DIMension" and originated in **Mari** (The
Foundry's texture-painting application), where it was developed to let artists
paint extremely high-resolution textures across a character's entire surface
using a single material.

UDIMs are now supported across essentially all professional 3D and texturing
software -- Maya, Houdini, Blender, Substance Painter, Mudbox, ZBrush, Arnold,
Redshift, RenderMan, and others.

The idea is simple: UV space is divided into a regular grid of 1x1 tiles. Each
tile is one unit wide and one unit tall. The tile sitting in the normal 0-to-1
range is the first tile. Going right along U gives more tiles in the same row;
going up along V gives the next row. Each tile gets a number, and that number
is used in the texture file name. The renderer looks up which tile a given UV
coordinate falls into and loads the corresponding file.

> *[Image needed: a diagram of the UDIM grid -- a grid of roughly 4 columns by
> 3 rows, each tile labeled with its UDIM number (1001, 1002 ... 1010, 1011,
> 1012 ... etc.), with U and V axes labeled and the origin (0,0) clearly marked
> at the bottom left.]*



### The UDIM Numbering System

Tiles are numbered starting at **1001** in the lower-left corner of UV space
(the tile covering U 0-to-1, V 0-to-1). The count goes left to right across
each row, and each row holds exactly **10 tiles**. At the end of a row the
count carries over to the next row up.

The formula for a tile's UDIM number is:

```
UDIM = 1001 + U_column + (V_row x 10)
```

Where `U_column` is the 0-based column position (0 through 9, left to right)
and `V_row` is the 0-based row position (0, 1, 2 ... going upward).

The first three rows look like this:

```
V row 2:  1021  1022  1023  1024  1025  1026  1027  1028  1029  1030
V row 1:  1011  1012  1013  1014  1015  1016  1017  1018  1019  1020
V row 0:  1001  1002  1003  1004  1005  1006  1007  1008  1009  1010
          U=0   U=1   U=2   U=3   U=4   U=5   U=6   U=7   U=8   U=9
```

A few examples to make this concrete:

- A UV at coordinate (0.3, 0.7) falls in column 0, row 0.
  UDIM = 1001 + 0 + (0 x 10) = **1001**

- A UV at coordinate (1.8, 0.2) falls in column 1, row 0.
  UDIM = 1001 + 1 + (0 x 10) = **1002**

- A UV at coordinate (0.5, 1.4) falls in column 0, row 1.
  UDIM = 1001 + 0 + (1 x 10) = **1011**

- A UV at coordinate (2.2, 2.9) falls in column 2, row 2.
  UDIM = 1001 + 2 + (2 x 10) = **1023**

To go the other direction -- if you know the UDIM number and want to find which
column and row it corresponds to:

```
offset   = UDIM - 1001
U_column = offset mod 10       (the remainder when dividing by 10)
V_row    = offset div 10       (the whole number result of dividing by 10)
```

Example: UDIM 1034
- offset = 1034 - 1001 = 33
- U_column = 33 mod 10 = 3  (column 3, tile covers U 3.0 to 4.0)
- V_row    = 33 div 10  = 3 (row 3, tile covers V 3.0 to 4.0)



### UDIM File Naming

Each tile corresponds to a separate image file on disk. The naming convention
embeds the UDIM number in the filename:

```
textureName.<UDIM>.extension
```

A character's skin color (diffuse/albedo) texture spread across four tiles
would produce files like:

```
charSkin_diffuse.1001.exr
charSkin_diffuse.1002.exr
charSkin_diffuse.1011.exr
charSkin_diffuse.1012.exr
```

When you point your material at `charSkin_diffuse.<UDIM>.exr`, the software
treats `<UDIM>` as a placeholder and fills in the actual number when loading
each tile. You do not load each file individually -- you load one path with the
token in it and the software finds all the matching files automatically.

> *[Image needed: a file browser showing a realistic set of UDIM texture files
> for a character -- diffuse, roughness, and normal maps all numbered with UDIM
> tiles -- to show what a set of UDIM textures looks like on disk.]*

In texture-painting software like Substance Painter or Mari, you can paint
directly across tile boundaries. The software knows which tile each brush stroke
lands on and writes the paint into the correct file.

> *[Image needed: a screenshot of a character in a texture-painting application
> (Substance Painter or Mari) showing the UV tiles laid out and paint work in
> progress with multiple tiles visible.]*



### Why Use Multiple Tiles?

The most common reason is resolution. A single texture file can only be so large
before it becomes impractical. A 4K texture (4096 x 4096 pixels) covers a lot
of surface area, but sometimes it is not enough -- particularly for a character
whose face needs to hold up in extreme close-up.

With UDIMs, you can put the head on one tile and the body on another. Both tiles
can be full 4K images. The model effectively has 8K by 4K worth of texture coverage
even though no single file exceeds 4K. This was one of the primary reasons UDIMs
became standard in film production. (As image resolutions have grown, the
constraint is less pressing, but the workflow remains standard.)

A secondary reason is organisation. Painting the face is a different job from
painting the clothing. Keeping them on separate tiles keeps the files separate
and makes it easier to divide work between artists or to iterate on one region
without touching the others.

> *[Image needed: a character's UV layout spread across a 2x2 grid of UDIM
> tiles -- head on one tile, body on another, limbs on others -- showing a
> typical film character UDIM layout.]*




Column Row Offset Format
----------------------

(This is Autodesk Maya's default format, and has been used by many other apps as well.)


This naming convention for UV tiles is an alternative to the UDIM
standard. Rather than encoding the tile position into a single number, Maya
writes the column and row explicitly:

```
u<column>_v<row>
```


The column row offset format simply specifies the range by how far it is offset (moved) from the initial zero to one range.


The naming of PNG file textures in this format looks like the following:

    texture_name.u<column>_v<row>.png


### Default Zero to One Range in both U and V

For the default 0 to 1 range in u and v, since the 1st column of the 1st row has zero offset in u or v, it would be

    u0_v0


The matching texture name would be:

    texture_name.u0_v0.png   (by comparison, UDIM format would be texture_name.1001.png)


### Next Column, U is Offset by One

(meaning the range is moved horizontally, to the right, by 1.0)
	 
The next column's range, which would be offset 1 to the right in the UV editor, would be written as:

    u1_v0


The matching texture file name would be something like:

    texture_name.u1_v0.png

	
In all cases we are assuming the individual ranges, the UV tiles, have width and height of 1.

So, this is really referring to the same underlying grid as would be used by UDIMs.
The tile that UDIM calls 1001 is what Maya
calls `u0_v0`. The column and row values are the same `U_column` and `V_row`
from the UDIM formula -- Maya just writes them out directly.

UDIM is a simpler looking format, it's just one number, no underscores or letters, easier to remember.

Column & Row format is more obvious.

Users of UDIM have to know the UDIM standard and what the numbers mean.

By contrast, someone who had never heard of column & row offset format would be able to figure it out pretty quickly if they found a bunch of files named in that format.

So, UDIM is simpler to remember a tile's number but harder to remember how it works, and column row has a more complex name, not just a number, but that name makes it much more obvious how the naming works. Different trade-offs were made in designing both standards.

```
Maya name    UDIM    Tile covers
u0_v0        1001    U: 0-1,  V: 0-1
u1_v0        1002    U: 1-2,  V: 0-1
u2_v0        1003    U: 2-3,  V: 0-1
u9_v0        1010    U: 9-10, V: 0-1
u0_v1        1011    U: 0-1,  V: 1-2
u1_v1        1012    U: 1-2,  V: 1-2
u3_v2        1024    U: 3-4,  V: 2-3
```

When Maya loads a texture using the `<UVTILE>` token in the file path, it
substitutes the tile's `u<column>_v<row>` name. The same four tiles from the
UDIM example above would be named:

```
charSkin_diffuse.u0_v0.exr     (= UDIM 1001)
charSkin_diffuse.u1_v0.exr     (= UDIM 1002)
charSkin_diffuse.u0_v1.exr     (= UDIM 1011)
charSkin_diffuse.u1_v1.exr     (= UDIM 1012)
```

Note that Maya can also load files using standard UDIM numbering -- you can set
the texture attribute to use `<UDIM>` instead of `<UVTILE>` if your files are
named with UDIM numbers. The `<UVTILE>` token is Maya's older default.



### Converting Between the Two Formats

Both systems describe exactly the same grid.

**Maya name to UDIM:**

```
UDIM = 1001 + U_column + (V_row x 10)
```

For `u3_v1`: UDIM = 1001 + 3 + (1 x 10) = **1014**

**UDIM to Maya name:**

```
offset   = UDIM - 1001
U_column = offset mod 10
V_row    = offset div 10
Maya name = u<U_column>_v<V_row>
```

For UDIM 1019:
- offset = 18
- U_column = 18 mod 10 = 8
- V_row = 18 div 10 = 1
- Maya name: **u8_v1**

The two formats are completely interchangeable. If you are working across
software that uses both and a texture isn't showing up where you expected it,
double-checking whether the file names match what the software is looking for
(UDIM number vs. Maya tile name) is usually the first thing to verify.


### Token Syntax by Software

The placeholder token varies between applications:

```
Software                   Token
------------------------------------------------------
Industry standard / Mari   <UDIM>
Maya (UDIM mode)           <UDIM>
Maya (UV Tile mode)        <UVTILE>
Houdini                    %(UDIM)d  or  <UDIM>
Blender                    <UDIM>
Substance Painter export   configurable, typically <UDIM>
```

When in doubt, `<UDIM>` is the most universally understood convention. If a
piece of software does not accept it, check its documentation for the specific
token it expects.




Ordinal names
-----------------------

In many cases, artists will talk about these, so they get a lot of colloquial use even though they aren't commonly used as a standard.

The 1st UDIM is UDIM 1001, and is offset from the default 0 to 1 range by 0.0 in both U and V.

So it's easy to talk about the texture of UDIM 1001 as "the first UDIM" or "the first UV tile". People do this all the time without even thinking about it. Part of what makes UDIMs easier to remember is that 1 corresponds to the 1 at the end of the number 1001, the first UDIM.

If someone says "the texture on the second UV tile", they are almost certainly talking about UDIM 1002, or column/row u1_v0.

Usually when people casually talk about textures (using these "ordinals" they are talking about low offsets, and they only say the ordinal of the U direction, while V is assumed to be zero. Someone usually would just say, "The third UV tile" not "The third UV tile of the first row".


To go from an ordinal name, to an offset based name, just subtract 1 from each direction, u & v.

u_2nd_v_1st  becomes  u1_v0  which is 1002 in UDIM format. They are all different ways of saying/writing the same information.




### Example of Ordinal to Offset Conversion

Since the rows and columns could be called 1st, 2nd, 3rd etc

In both U and V (positive)...

The 1st is offset 0
The 2nd is offset 1
The 3rd is offset 2
etc

*(section incomplete)*
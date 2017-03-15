# TESX File Spec #

# About

TESX is a portable .xml file that represents a tessellation usable in [nTpology Element Pro](http://www.ntopology.com/element-pro/). A tessellation is defined by a number of closed polyhedra & parent to child relationships between those closed polyhedra. A parent is one polyhedra, while a child is a polyhedra plus a 4x4 matrix representing an affine transformation.

# Types

## tessellation
A tessellation is the main XML TAG & contains **units** & **rules** -- One tessellation is enough information to build the scaffold of a lattice in Element.

#### Attributes:
* name, string to represent the name of the entire tessellation

## units
An array of closed polyhedra, each represented by a **unit**. It is here where the data for each unique closed polyhedra is stored. For example, if the tessellation is for a cubic grid, there would be only one unit needed, the cube, even though the tessellation shows 6 cubes as children & one cube as parent. The unit is defined in local coordinates.

## unit
One closed polyhedra represented by a [Face-vertex mesh](https://en.wikipedia.org/wiki/Polygon_mesh#/media/File:Mesh_fv.jpg) (*note* however, the faces here can have any number of sides) containing **vertices** & **faces**

## vertices
An array of 3D points, each point contained within a **vertex**

## vertex
A 3-dimensional vector representing a point in 3D space.

#### Attributes:
* x, a double
* y, a double
* z, a double

## faces
An array of n-sided polygon faces: **face**

## face
An array of **face_vert**

## face_vert
An integer index to a **vertex** (Zero based numbering)

#### Attributes:
* n, an integer

_______________________________________________________________________________

## rules
An array of **rule** -- usually there is at least one **rule** per **unit** however, this is not always the case.

## rule
One parent unit and multiple **child** units in **children**. The children units additionally contain a 4x4 matrix that represents the affine transformation of the child from the parent. Usually a rule will contain one child for every face in the parents polyhedra, but this is not always the case.

#### Attributes:
* name, a string

## parent
The parent unit represented as an integer index into the list of **units** (Zero based numbering)

#### Attributes:
* unit, an integer

## children
An array of **child** units

## child
One child unit represented as an integer index into the list of **units** (Zero based numbering) with the addition of a 4x4 matrix, **mat4** which represents an affine transformation from the parent. A child unit is located in a different position with a potentially different scale & rotation from the parent.

#### Attributes:
* unit, an integer

## mat4
An affine transformation represented in a 4x4 matrix, row-major ordering :

|  aa  ab  ac  ad  |
|  ba  bb  bc  bd  |
|  ca  cb  cc  cd  |
|  da  db  dc  dd  |

#### Attributes:
*aa, a double [0][0] in the matrix
*ab, a double [0][1] in the matrix
*ac, a double [0][2] in the matrix
*ad, a double [0][3] in the matrix

*ba, a double [1][0] in the matrix
*bb, a double [1][1] in the matrix
*bc, a double [1][2] in the matrix
*bd, a double [1][3] in the matrix

*ca, a double [2][0] in the matrix
*cb, a double [2][1] in the matrix
*cc, a double [2][2] in the matrix
*cd, a double [2][3] in the matrix

*da, a double [3][0] in the matrix
*db, a double [3][1] in the matrix
*dc, a double [3][2] in the matrix
*dd, a double [3][3] in the matrix

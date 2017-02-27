### /* Copyright 2016 nTopology Inc. All Rights Reserved.
###
### TESX writer v1.0.0
###
### Notes:
### Currently, this script is used to export a custom tessellation from Rhino. The script is setup
### to write out a tessellation with all of the same unit topologies, even though the file spec allows
### for multiple unit types.

import rhinoscriptsyntax as rs
import scriptcontext
import math
import Rhino

import clr
clr.AddReference("System.Xml")
import System.Xml

tesXVersion = "1.0.0"

mat4XML = [[ "aa", "ab","ac","ad" ], [ "ba", "bb","bc","bd" ],[ "ca", "cb","cc","cd" ],[ "da", "db","dc","dd" ] ]

def main():
    rulename = rs.GetString("Input Rule Name","New Rule")
    parentIn = rs.GetObject("select Parent",16)
    childrenIn = rs.GetObjects("Select children", 16)

    parent = rs.CopyObject(parentIn)
    children = rs.CopyObjects(childrenIn)
    parentChildren = [parent,children]
#Check to see if the user wants to normalize the units?
    items = ("Normalize", "No", "Yes")
    doNormalize = rs.GetBoolean("Boolean options", items, (True) )
    if doNormalize[0]:
        parentChildren = normalizeBreps(parentChildren[0], parentChildren[1])

    #create a filename variable
    #prompt the user to specify a file name
    filter = "Tessellation XML File (*.tesx)|*.tesx|All files (*.*)|*.*||"
    filename = rs.SaveFileName("Save Tessellation XML File As", filter)
    if not filename: return
    XMLExport(filename,rulename, parentChildren[0], parentChildren[1])

    rs.DeleteObject(parent)
    rs.DeleteObjects(children)

def normalizeBreps(parent, children):
    boxPts = rs.BoundingBox(parent)
    box = Rhino.Geometry.BoundingBox(boxPts)
    cntr = pCntr = rs.SurfaceAreaCentroid(parent)[0]
    maxExtent = max(box.Diagonal)
    rs.MoveObject(parent, -cntr)
    rs.MoveObjects(children, -cntr)
    scaleInv = 1/maxExtent
    rs.ScaleObject(parent,[0,0,0],[scaleInv,scaleInv,scaleInv])
    rs.ScaleObjects(children,[0,0,0],[scaleInv,scaleInv,scaleInv])
    return [parent,children]


def ExtractPtsFaces(brep):
    verts = brep.Vertices
    faces = brep.Faces

    ptArray = []
    for v in verts:
        loc = v.Location
        ptArray.append(loc)

    faceArray = []
    for f in faces:
        loop = f.OuterLoop
        curve = loop.To3dCurve()
        pts = rs.PolylineVertices(curve)
        faces = []
        for pt in range(0, len(pts)-1):
            for i in range(0, len(ptArray)):
                if rs.PointCompare(pts[pt],ptArray[i]):
                    faces.append(i)
                    break
        faceArray.append(faces)
    return [ptArray, faceArray]

def getTransform(parent, child):
    pCntr = rs.SurfaceAreaCentroid(parent)[0]
    pArea = rs.SurfaceArea(parent)

    cArea = rs.SurfaceArea(child)
    scaleVal =math.sqrt( cArea[0] / pArea[0])
    s = rs.XformScale(scaleVal, pCntr)
    cCntr = rs.SurfaceAreaCentroid(child)[0]
    t = rs.XformTranslation(cCntr-pCntr)
    matrixF = t
    if scaleVal!=1:
        matrixF = rs.XformMultiply(matrixF, s)
    return matrixF

def WriteUnit(writer, brep):
    unit = ExtractPtsFaces(brep)
    ptArray = unit[0]
    faceArray = unit[1]

    writer.WriteStartElement("unit")
    writer.WriteStartElement("vertices")
    #write vertices here:
    for pt in ptArray:
        writer.WriteStartElement("vertex")
        writer.WriteAttributeString("x", str(pt[0]))
        writer.WriteAttributeString("y", str(pt[1]))
        writer.WriteAttributeString("z", str(pt[2]))
        writer.WriteEndElement()
    writer.WriteEndElement()

    #Write faces here:
    writer.WriteStartElement("faces")
    for face in faceArray:
        #write each face here:
        writer.WriteStartElement("face")
        for f in face:
            writer.WriteStartElement("face_vert")
            writer.WriteAttributeString("n", str(f))
            writer.WriteEndElement()
        writer.WriteEndElement()
    writer.WriteEndElement()

    writer.WriteEndElement()

def WriteUnits(writer, brep):
    writer.WriteStartElement("units")
    WriteUnit(writer, brep)
    writer.WriteEndElement()

def WriteRule(writer, name, parent, children):
    writer.WriteStartElement("rule")
    writer.WriteAttributeString("name", name)

    writer.WriteStartElement("parent")
    writer.WriteAttributeString("unit", "0")
    writer.WriteEndElement()
    writer.WriteStartElement("children")
    for child in children:
        xform = getTransform(parent,child)
        writer.WriteStartElement("child")
        writer.WriteAttributeString("unit", "0")
        writer.WriteStartElement("mat4")
        for i in range (0,4):
            for j in range(0,4):
                writer.WriteAttributeString(mat4XML[i][j], str(xform[j,i]))
        writer.WriteEndElement()
        writer.WriteEndElement()
    writer.WriteEndElement()
    writer.WriteEndElement()

def WriteRules(writer,name, parent, children):
    writer.WriteStartElement("rules")
    WriteRule(writer,name, parent, children)
    writer.WriteEndElement()

def XMLExport(filename,rulename, parent, children):
    settings = System.Xml.XmlWriterSettings()
    settings.Indent = True
    writer = System.Xml.XmlWriter.Create (filename, settings)

    writer.WriteComment(".tesx file" +tesXVersion+" exported from Rhino")
    #Write an element (this one is the root).
    writer.WriteStartElement("tessellation")
    writer.WriteAttributeString("name", rulename)

    brep = rs.coercebrep(parent)

    WriteUnits(writer,brep)
    WriteRules(writer,rulename, parent, children)

    writer.Close()


if __name__=="__main__":
    main()
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


def main():
    rulename = rs.GetString("Input Rule Name","New Rule")
    parent1 = rs.GetObject("select Parent",16)
    children1 = rs.GetObjects("Select children", 16)

    #create a filename variable
    filename = rs.SaveFileName("Save CSV file","*.csv||", None, rulename, "csv")

    #open the file for writing
    file = open(filename, 'w')


    brep = rs.coercebrep(parent1)

    verts = brep.Vertices
    faces = brep.Faces

    ptArray = []
    for v in verts:
        loc = v.Location
        ptArray.append(loc)

    file.write("vertices," + str(len(ptArray)))
    file.write("\n")
    for pt in ptArray:
        file.write(str(pt))
        file.write("\n")

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


    file.write("faces," + str(len(faceArray)))
    file.write("\n")

    for face in faceArray:
        file.write(str(face))
        file.write("\n")



    pCntr1 = rs.SurfaceAreaCentroid(parent1)[0]
    pArea1 = rs.SurfaceArea(parent1)

    file.write("children_1," + str(len(children1)))
    file.write("\n")

    for child in children1:
        areaC1 = rs.SurfaceArea(child)
        scaleVal =math.sqrt( areaC1[0] / pArea1[0])
        cntr = rs.SurfaceAreaCentroid(child)[0]
        t = rs.XformTranslation(cntr-pCntr1)
        matrixF = t

        file.write(str(matrixF))
        file.write("\n")

    file.close()

def XMLTest():
    filename = r"C:\Users\Phoenix\Desktop\testWrite.tesx"
    xmldoc = System.Xml.XmlDocument()
    xmldoc.Load(filename)
    items = xmldoc.SelectNodes("tessellation/units/unit")
    for item in items:
        print item.InnerText
    XMLExport()

def WriteUnit(writer):
    writer.WriteStartElement("unit")

    writer.WriteStartElement("vertices")
    #write vertices here:
    writer.WriteStartElement("vertex")
    writer.WriteAttributeString("x", "-0.5")
    writer.WriteAttributeString("y", "-0.5")
    writer.WriteAttributeString("z", "-0.5")
    writer.WriteEndElement()
    writer.WriteEndElement()

    #Write faces here:
    writer.WriteStartElement("faces")
    #write vertices here:
    writer.WriteStartElement("face")
    writer.WriteStartElement("face_vert")
    writer.WriteAttributeString("n", "3")
    writer.WriteEndElement()
    writer.WriteEndElement()
    writer.WriteEndElement()

    writer.WriteEndElement()


def WriteUnits(writer):
    writer.WriteStartElement("units")
    WriteUnit(writer)
    writer.WriteEndElement()

def WriteRule(writer):
    writer.WriteStartElement("rule")
    writer.WriteAttributeString("name", "Hex Prism")

    writer.WriteStartElement("parent")
    writer.WriteAttributeString("unit", "3")
    writer.WriteEndElement()

    #Write faces here:
    writer.WriteStartElement("children")
    #write vertices here:
    writer.WriteStartElement("child")
    writer.WriteAttributeString("unit", "1")
    writer.WriteStartElement("mat4")
    writer.WriteAttributeString("aa", "3.1")
    writer.WriteEndElement()
    writer.WriteEndElement()
    writer.WriteEndElement()

    writer.WriteEndElement()

def WriteRules(writer):
    writer.WriteStartElement("rules")
    WriteRule(writer)
    writer.WriteEndElement()

def XMLExport():
    #prompt the user to specify a file name
    filter = "Tessellation XML File (*.tesx)|*.tesx|All files (*.*)|*.*||"
    filename = rs.SaveFileName("Save Tessellation XML File As", filter)
    if not filename: return

    settings = System.Xml.XmlWriterSettings()
    settings.Indent = True
    writer = System.Xml.XmlWriter.Create (filename, settings)

    writer.WriteComment(".tesx file" +tesXVersion+" exported from Rhino")

    #Write an element (this one is the root).
    writer.WriteStartElement("tessellation")
    WriteUnits(writer)
    WriteRules(writer)
#
#    #Write the namespace declaration.
#    writer.WriteAttributeString("xmlns", "bk",None , "urn:samples")
#
#    #Write the genre attribute.
#    writer.WriteAttributeString("genre", "novel")
#
#    #Write the title.
#    writer.WriteStartElement("title")
#    writer.WriteString("The Handmaid's Tale")
#    writer.WriteEndElement()
#
#    #Write the price.
#    writer.WriteElementString("price", "19.95")
#
#    #Lookup the prefix and write the ISBN element.
#    prefix = writer.LookupPrefix("urn:samples")
#    writer.WriteStartElement(prefix, "ISBN", "urn:samples")
#    writer.WriteString("1-861003-78")
#    writer.WriteEndElement()
#
#    #Write the style element (shows a different way to handle prefixes).
#    writer.WriteElementString("style", "urn:samples", "hardcover")
#
#    #Write the close tag for the root element.
#    writer.WriteEndElement()
#
#    #Write the XML to file and close the writer.
    writer.Flush()
    writer.Close()
#
#    writer = System.Xml.XmlTextWriter(filename, System.Text.UTF8Encoding(True, True))
#    writer.WriteStartDocument()
#    writer.WriteStartElement("car")
#    writer.WriteElementString("name", "Jaguar")
#    writer.WriteEndElement()
#    writer.WriteEndDocument()
#    writer.Close()

if __name__=="__main__":
    main()
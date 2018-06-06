from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Parameter

import sys
from lxml import etree

app = Flask(__name__)

engine = create_engine('sqlite:///partool.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

tree = etree.parse('PA_T04.cnf.xml')
nsmap = {'ns': 'x-schema:ConfigFileSchema.xml'}
tagname = tree.xpath('ns:Block/ns:BlockDef/ns:BlockName', namespaces = nsmap)[0].text

# MultiBlock Configuration Properties
xConfigs = tree.xpath('ns:Block/ns:BlockDef', namespaces = nsmap)
xCoords = tree.xpath('ns:Block/ns:BlockDef/ns:Coord', namespaces = nsmap)

for xConfig in xConfigs:
    for ChildNode in xConfig.getchildren():
        if ChildNode.tag.split('}', 1)[1] <> "Coord":
            #print(tagname, tagname, ChildNode.tag.split('}', 1)[1], ChildNode.text)
            newParam = Parameter(tagname = tagname, blockname = tagname, blocktype = "", paramname = ChildNode.tag.split('}', 1)[1], paramvalue = ChildNode.text, paramtype = "")
            session.add(newParam)
            
for xCoord in xCoords:
        for ChildNode in xCoord.getchildren():
            xParamType = ChildNode.tag.split('}', 1)[1]
            if xParamType == "Left":
                xS1 = ChildNode.text
            elif xParamType == "Top":
                xS2 = ChildNode.text
            elif xParamType == "Right":
                xS3 = ChildNode.text
            elif xParamType == "Bottom":
                xS4 = ChildNode.text
                #print(tagname, tagname, "Coord", "L=" + xS1 + ",T=" + xS2 + ",R=" + xS3 + ",B=" + xS4 )
                newParam = Parameter(tagname = tagname, blockname = tagname, blocktype = "", paramname = "Coord", paramvalue = "L=" + xS1 + ",T=" + xS2 + ",R=" + xS3 + ",B=" + xS4, paramtype = "")
                session.add(newParam)

# MultiBlock Parameters

xParameters = tree.xpath('ns:Block/ns:Parameters/ns:Parameter', namespaces = nsmap)
for xParameter in xParameters:
    for ChildNode in xParameter.getchildren():
        xParamType = ChildNode.tag.split('}', 1)[1]
        if xParamType == "ParamName":
            xParamName = ChildNode.text
        elif xParamType == "ParamValue":
            xParamValue = ChildNode.text
            #print(tagname, tagname, xParamName, xParamValue)
            newParam = Parameter(tagname = tagname, blockname = tagname, blocktype = "", paramname = xParamName, paramvalue = xParamValue, paramtype = "")
            session.add(newParam)

#Block Parameters / Connections / Symbol Attributes
i = 1 #Block Iteration
xS0 = ""; xS1 = ""; xS2 = ""; xS3 = ""; xS4 = ""; xS5 = "" #Symbol Attribute Strings

xBlocks = tree.find('ns:Block/ns:EmbBlocks/ns:Block', namespaces = nsmap)

for xBlock in xBlocks:
    block = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:BlockDef/ns:BlockName'.format(i), namespaces = nsmap)[0].text
    xConfigs = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:BlockDef'.format(i), namespaces = nsmap)
    xCoords = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:BlockDef/ns:Coord'.format(i), namespaces = nsmap)
    xParameters = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:Parameters/ns:Parameter'.format(i), namespaces = nsmap)
    xSymbolAttrs = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:SymbolAttrs/ns:SymbolAttr'.format(i), namespaces = nsmap)
    xConnections = tree.xpath('ns:Block/ns:EmbBlocks/ns:Block[{0}]/ns:Connections/ns:Connection'.format(i), namespaces = nsmap)

    for xConfig in xConfigs:
        for ChildNode in xConfig.getchildren():
            if ChildNode.tag.split('}', 1)[1] <> "Coord":
                #print(tagname, block, ChildNode.tag.split('}', 1)[1], ChildNode.text)
                newParam = Parameter(tagname = tagname, blockname = block, blocktype = "", paramname = ChildNode.tag.split('}', 1)[1], paramvalue = ChildNode.text, paramtype = "")
                session.add(newParam)
                        
    for xCoord in xCoords:
        for ChildNode in xCoord.getchildren():
            xParamType = ChildNode.tag.split('}', 1)[1]
            if xParamType == "Left":
                xS1 = ChildNode.text
            elif xParamType == "Top":
                xS2 = ChildNode.text
            elif xParamType == "Right":
                xS3 = ChildNode.text
            elif xParamType == "Bottom":
                xS4 = ChildNode.text
                #print(tagname, block, "Coord", "L=" + xS1 + ",T=" + xS2 + ",R=" + xS3 + ",B=" + xS4 )
                newParam = Parameter(tagname = tagname, blockname = block, blocktype = "", paramname = "Coord", paramvalue = "L=" + xS1 + ",T=" + xS2 + ",R=" + xS3 + ",B=" + xS4, paramtype = "")
                session.add(newParam)
                
    for xParameter in xParameters:
        for ChildNode in xParameter.getchildren():
            xParamType = ChildNode.tag.split('}', 1)[1]
            if xParamType == "ParamName":
                xParamName = ChildNode.text
            elif xParamType == "ParamValue":
                xParamValue = ChildNode.text
                #print(tagname, block, xParamName, xParamValue)
                newParam = Parameter(tagname = tagname, blockname = block, blocktype = "", paramname = xParamName, paramvalue = xParamValue, paramtype = "")
                session.add(newParam)

    for xSymbolAttr in xSymbolAttrs:
        for ChildNode in xSymbolAttr.getchildren():
            xParamType = ChildNode.tag.split('}', 1)[1]
            if xParamType == "ParamName":
                xS0 = ChildNode.text.split('.', 2)[2]
            elif xParamType == "AttrType":
                xParamName = xS0 + "(" + ChildNode.text +")"
            elif xParamType == "AttrOrder":
                xS1 = ChildNode.text
            elif xParamType == "AttrViewValue":
                xS2 = ChildNode.text
            elif xParamType == "AttrViewLabel":
                xS3 = ChildNode.text
            elif xParamType == "XCoord":
                xS4 = ChildNode.text
            elif xParamType == "YCoord":
                xS5 = ChildNode.text
                #print(tagname, block, xParamName, xS1 + ", " + xS2 + ", " + xS3 + ", " + xS4 + ", " + xS5)
                newParam = Parameter(tagname = tagname, blockname = block, blocktype = "", paramname = xParamName, paramvalue = xS1 + ", " + xS2 + ", " + xS3 + ", " + xS4 + ", " + xS5, paramtype = "")
                session.add(newParam)

    for xConnection in xConnections:
        for ChildNode in xConnection.getchildren():
            xParamType = ChildNode.tag.split('}', 1)[1]
            if xParamType == "InputEnd":
                xParamName = ChildNode.text.split('.', 2)[2] + "(Connection)"
            elif xParamType == "OutputEnd":
                xParamValue = ChildNode.text
                #print(tagname, block, xParamName, xParamValue)
                newParam = Parameter(tagname = tagname, blockname = block, blocktype = "", paramname = xParamName, paramvalue = xParamValue, paramtype = "")
                session.add(newParam)

    i = i + 1

session.commit()
session.query(Parameter).all()

            
        

        

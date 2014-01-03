#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Solution for Lab 7, GIS 450
#
# Author:      rjarvis
#
# Created:     31/10/2013
# Copyright:   (c) rjarvis 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os, sys
arcpy.env.overwriteOutput = True
try:
    # shapefile created

    # get user input
    inputFeatures = arcpy.GetParameterAsText(0)
    railroad = arcpy.GetParameterAsText(1)
    railroadDistance = arcpy.GetParameterAsText(2)
    roads = arcpy.GetParameterAsText(3)
    roadsDistance = arcpy.GetParameterAsText(4)
    school = arcpy.GetParameterAsText(5)
    schoolDistance = arcpy.GetParameterAsText(6)
    streams = arcpy.GetParameterAsText(7)
    streamsDistance = arcpy.GetParameterAsText(8)
    parks = arcpy.GetParameterAsText(9)
    parksDistance = arcpy.GetParameterAsText(10)
    outputGB = arcpy.GetParameterAsText(11)
    finalClass = arcpy.GetParameterAsText(12)

    arcpy.env.workspace = outputGB

    # tool time

    points = outputGB + "\\points"
    # get the input features as points
    finalPoints = arcpy.CopyFeatures_management(inputFeatures, points)
    # lets make a layer
    arcpy.MakeFeatureLayer_management(finalPoints, "FinalPointsLyr")
    # buffer the railroad
    railroadBuffer = outputGB + "\\railroadBuffer"
    arcpy.Buffer_analysis(railroad, railroadBuffer, railroadDistance, "FULL" , "ROUND", "ALL", "")
    # buffer the roads
    roadsBuffer = outputGB + "\\roadsBuffer"
    arcpy.Buffer_analysis(roads, roadsBuffer, railroadDistance, "FULL" , "ROUND", "ALL", "")
    # buffer the school
    schoolBuffer = outputGB + "\\schoolBuffer"
    arcpy.Buffer_analysis(school, schoolBuffer, schoolDistance, "FULL", "ROUND", "ALL", "")
    # buffer streams
    streamsBuffer = outputGB + "\\streamBuffer"
    arcpy.Buffer_analysis(streams, streamsBuffer, streamsDistance, "FULL", "ROUND", "ALL", "")
    # buffer parks
    parksBuffer = outputGB + "\\parksBuffer"
    arcpy.Buffer_analysis(parks, parksBuffer, parksDistance, "FULL", "ROUND", "ALL", "")
    # adding layers, layers added based on the ones within and not within

    # within
    withinBuffered = arcpy.Merge_management([railroadBuffer, roadsBuffer], outputGB + "\\withinBuffered")

    # must not be within
    notWithin = arcpy.Merge_management([schoolBuffer, streamsBuffer, parksBuffer], outputGB + "\\notWithin")

    # what to erase
    eraseStuff = finalClass

    # erase stuff
    arcpy.Erase_analysis(withinBuffered,notWithin, eraseStuff, "")

    # make a layer with erase stuff
    arcpy.MakeFeatureLayer_management(eraseStuff, "SuitabilityLyr")

    # select by location
    suitability = arcpy.SelectLayerByLocation_management("FinalPointsLyr", "WITHIN", eraseStuff)

    # take the location of all landfills that have a suitable location
    dumps = outputGB + "\\avail_landfills"

    # copy the suitability features to the dumps for final suitabilty
   # finalSuitability = outputGB + "\\finalSuitability"

    finalClass = arcpy.CopyFeatures_management(suitability, dumps)

except arcpy.ExecuteError:
    # Get the tool error messages
    #
    msgs = arcpy.GetMessages(2)

    # Return tool error messages for use with a script tool
    #
    arcpy.AddError(msgs)

    # Print tool error messages for use in Python/PythonWin
    #
    print msgs

except:
    # Get the traceback object
    #
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    #
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    # Return python error messages for use in script tool or Python Window
    #
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)

    # Print Python error messages for use in Python / Python Window
    #
    print pymsg + "\n"
    print msgs








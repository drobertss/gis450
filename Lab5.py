#-------------------------------------------------------------------------------
# Name:        Lab Five
# Purpose:     Solution to lab five for GIS 450
#
# Author:      rjarvis
#
# Created:     07/10/2013
# Copyright:   (c) rjarvis 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os, traceback, sys
arcpy.env.overwriteOutput = True
error = False
array = arcpy.Array()

try:
    # get user input for the location of the file geodatabase
    gb = raw_input("Please enter the location of the file geodatabase")


    # check it exists
    if arcpy.Exists(gb):
        print "The geodatabase exists, congratulations"
    else:
        # terminate if it doesnt
        print("The geodatabase does not exist, the program will now terminate")
        print sys.exit.__doc__

    # set the worksapce to the user input
    arcpy.env.workspace = gb
    print "The workspace is now set to " + gb

    # get rectangle coordinates
    xmin = raw_input("Please enter your XMIN coordinate")
    ymin = raw_input("Please enter your YMIN coordinate")
    xmax = raw_input("Please enter your XMAX coordinate")

    # make sure xmax is bigger than xmin
    if(xmax < xmin):
        error = True
        while error:
            xmax = raw_input("Please enter an XMAX greater than your XMIN")
            if(xmax>xmin):
                error = False


    ymax = raw_input("Please enter your YMAX coordinate")

    # make sure ymax is bigger than xmax
    if(ymin > ymax):
        error = True
        while error:
            ymax = raw_input("Please enter a YMAX greater than your YMIN")
            if(ymax>ymin):
                error = False

    # get feature classes from GB
    fcNames = arcpy.ListFeatureClasses("")

    # user extent
    extent = arcpy.Extent(xmin,ymin,xmax,ymax)

    #set extent to user extent
    arcpy.env.extent = extent

    #iterate through the feature classes in the gb
    for fc in fcNames:

        desc = arcpy.Describe(fc)

        extent2 = desc.Extent
        #find overlaps
        if(extent.overlaps(extent2) or extent.within(extent2) or extent.contains(extent2)):
            count = arcpy.GetCount_management(fc)
            print (fc+ " overlaps: ")
            print "There were " + str(count) + " overlaps."




except arcpy.ExecuteError:
    # Get the tool error messages
    #
    msgs = arcpy.GetMessages(2)

    # Return tool error messages for use with a script tool
    #
    arcpy.AddError(msgs)

    # Print tool error messages for use in Python/PythonWin
    #
    print (msgs)

except:
    # Get the traceback object
    #
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    #
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

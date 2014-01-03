#-------------------------------------------------------------------------------
# Name:       Lab 3
# Purpose:
#
# Author:      Rob Jarvis
#
# Created:     19/09/2013
# Copyright:   (c) Rob 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, traceback, sys, os
arcpy.env.overwriteOutput = True

try:
    #  Get information from user using raw_input statements and storing in variables

    #feature class that will be buffered
    featureClass = raw_input("Enter the file location of the Feaure Class you wish to buffer")

    # output geodatabase to write at to
    outputGB = raw_input("Enter the file location of the geodatabase you wish to write the output data to")

    # feature class that is going to be clipped
    featureClassClip = raw_input("Please enter the file location of the feature class you wish to clip")

    # name of the integer field
    integerField = raw_input("Enter a name for the buffer field")

    # the value used for the buffer
    integerFieldValue = raw_input("Enter a value to calculate the buffer")



    #  Use arcpy.Exists statements to make sure user input valid pathnames to both Feature classes AND for the output File GDB location

    # does the feature class exist
    if arcpy.Exists(featureClass):
        print("The feature class that will be buffered file location exists")

    else:
        print("The feature class that will be buffered file location does not exist")
        sys.exit()

    # does the geodatabase exist
    if arcpy.Exists(outputGB):
        print("The geodatabase output file exists")

    else:
        print("The geodatbase output file does not exist")
        sys.exit()

    #does the feature class that will be clipped exist
    if arcpy.Exists(featureClassClip):
        print("The feature class that will be clipped exists")

    else:
        print("The feature class that will be clipped does not exist")
        sys.exit()


    #  Add Field to Feature Class

    arcpy.AddField_management(featureClass, integerField, "LONG")

    #  Calculate Field to value

    arcpy.CalculateField_management(featureClass, integerField, integerFieldValue)

    #  Create an output pathname string that will be used in the buffer, to include '_buff'

    # determine index length to see if last char is '\'
    outputGBLength = len(outputGB)


    #error handling in case user does not put a backslash at the end of their path
    if(outputGB[outputGBLength-1] != '\\'):
        bufferOutput = outputGB + "\\" + os.path.basename(featureClass) + "_buff"
    else:
        bufferOutput = outputGB +  os.path.basename(featureClass) + "_buff"
   #  print("The bufferOutput variable is set to " + bufferOutput)




    #  Buffer featureclass using Buffer field

    arcpy.Buffer_analysis(featureClass, bufferOutput, integerField)

    #  Create an output pathname string that will be clipped

    # get length of clip output
    clipOutputLength = len(featureClassClip)
    # print("First try: Clip Output Length = " + str(clipOutputLength))

    # clipOutput = os.path.basename(featureClassClip + "_buff")
    if(outputGB[outputGBLength-1] != '\\'):
        clipOutput = outputGB + "\\" + os.path.basename(featureClassClip) + "_clip"
    else:
        clipOutput = outputGB +  os.path.basename(featureClassClip) + "_clip"

    # print("Second try: Clip output" + clipOutput)

    #  Clip second featureclass by the buffer featureclass, to include '_clip'

    arcpy.Clip_analysis(bufferOutput, featureClassClip, clipOutput)

    #  Print message to user that the Script is complete
    print ("The script is complete!")

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

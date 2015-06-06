#Demag_GUI Usage and Tips (Version 3.2) 

##Launching

The Gui may be launched either with the command line by going to the directory containing demag_gui.py and running it with:

```bash
python ./demag_gui.py
```

If you have QuickMagIC already running you can launch demag_gui by just clicking on the demag_gui button in the main window shown below:

![](../images/QuickMagicLauncher.png)

##Interpretation of Specimen Data

###Adding Interpretations:  
You can analyze specimen component data by adding fits with the add fit button. Additionally you can select the fit you would like to edit or view by using the drop down box under the add fit button. Once you have selected a fit the shape of the selected fit's data points will turn to a diamond shape to distinguish them from the other data points.  
![](../images/FitBox.png)
  
Once you have selected the desired fit you can edit its bounds using the drop down boxes under the bounds header  
![](../images/BoundsBox.png)
  
Alternativly you can double click the list of measurement steps on the left to pick out the bounds of your interpertation. The included steps in the currently selected interpertation are shown in blue on this list and measurement steps marked bad are shown in yellow. (This method of selecting bounds is recomended for mac users who have in the past experinced problems with the drop down boxes)  
![](../images/Logger.png)
  
You may notice that the fit will be given a generic name such as *Fit 1* you can change the name of the fit from default by typing into the drop down box containing fits then pressing enter. You can anchor your interpertation or preform a plane fit using the drop down box under specimen mean type (default: line).  
![](../images/SpecimenMeanType.png)
  
Coordinate Systems available as well as orrientation of Zijderveld are available on the left.  
![](../images/ZijData.png)  

Specimen data for a fit can be seen in the upper center of the GUI in a large box labeled specimen mean statistics.  
![](../images/InterpData.png)
  
###Flagging Bad Measurment Data

You can set acceptance criteria to a pmag_criteria table by using Analysis/"Acceptance Criteria"/"Change Acceptance Criteria". If any measurement steps are bad you can flag them as such by right clicking on the list of measurement steps to the left of the GUI. If you flag a step bad that you would later like to restore you can simply right click on it again and it will be flagged as good again.

###Saving Specimen Interpretations

Once you have picked out your interpertations you can save the session data in two different ways a .redo file or pmag tables. In addition you may save image files of the plots.

####The .Redo File: 

You can use Analysis/"Save current interpertations to a redo file" to create this file type  or you can just hit the save button next to add fit, this method is recomended as it prevents accidental pressing of the clear all interpertations button. **Note:** this file type does **NOT** load previous interpertations on start up you must go to the menu option Analysis/"Import previous interpertations from a redo file" to restore your previous session.

####The Pmag Tables:

By going to the menu File/"Save MagIC pmag tables" you can export your interpertations made in Demag GUI to the MagIC pmag tables which can then be used by other MagIC programs or uploaded to the MagIC database. You can export any or all of the 3 coordinate systems upon selecting this option and you may choose to save pmag_samples, pmag_sites, and pmag_results tables in addition to the pmag_speciemns table that is output. If you choose to output additional information you will be prompted by a pop up window for additional information. **Note:** this save format loads on start up of the GUI imediatly restoring your session, also selection of this option will overwrite your demag_gui.redo file in the working directory.  

####Images of Plots:

Select the menu option File/"Save plot"/"Save all plots" to save all plots alternativly you can save any of the plots individually. Some examples can be seen below:

 ![Zijderveld with 3 interpertations](../images/Z35_1a_Zij.png)  
 ![Equal Area plot of specimen data and interpertations](../images/Z35_1a_EqArea.png)  
 ![M/M0](../images/Z35_1a_M_M0.png)  
 ![The Higher order mean plot with fisher mean for all specimens in study](../images/Z35_site.png)  \pagebreak


###Deleting Specimen Interpretations

If you would like to delete a single interpertation select the one you wish to delete from the interpertation drop down box then click delete. Alternativly if you wish to clear all interpertations you may go to the menu option Analysis/"Clear all current interpertations".  
![](../images/SaveDelete.png)  

##Higher Level Plots and Interpretation

The set of drop down boxes to the right of the interpertation data is there to determine what level you want to analyze in the higher level analysis options include: site, sample, location, and study. The drop down below this selects which of the available sites, samples, location, or studies you want to display.  
![](../images/HigherOrderOptions.png)

You can then select how to group your data by using the drop down menu under the show header. You can select what kind of mean to take using the first drop down under the mean header. Which interpertations to use for the means can be selected under the second drop down menu. You can then use the remove/replace button to remove or replace the set of points belonging to the current specimen in the higher order mean.  
![](../images/HigherOrderMeanOptions.png)

You can view the higher order stats results in the bottom left of the GUI.  
![](../images/HigherOrderMeanOutput.png)



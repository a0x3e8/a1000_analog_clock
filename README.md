#a1000 analog clock
______________________
this is a simple analog clock written in python language
using pygtk and pycairo.
it can be used as a stand alone widget or clock image 
creator for use in conky.
_______________________
#how to use:
with command line arguments you will be able to costumize the clock:
- -h shows the help message.
- -w [width] sets the width of the clock face.
- -H [height] sets the height of the clock face.
- -s visible second hand
- -i image mode.
if you want to use this clock in conky, you should call it with '-i' argument.
this switch will cause the program to create output as png image instead of 
rendering it in a gtk window.

##TODO:
- commandline arguments.
- colors
- remove widget mode background and caption


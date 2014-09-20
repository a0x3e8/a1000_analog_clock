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

## use in conky:
1)save .py file somewhere in your home directory.
2)open conkyrc file.
3)add following lines to file and save it:

```code
${execpi 0.8 python PATH//analog_clock.py -s -i -w 150 -H 150>/dev/null}
${image PATH/clock_face.png -p 30,330 -s 150x150}
```
PATH will be where you saved .py file.
how you will change this setting is up to you and your conky setting. these are my settings.
##TODO:
- commandline arguments.
- colors
- remove widget mode background and caption


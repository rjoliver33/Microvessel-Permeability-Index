# Microvessel Permeability Index

Microvessel Permeability Index is a Python program for the analysis of .tif microscopy images to determine the level of colocalization between dextran (Red Channel) with microvessels (Green Channel). This program was designed for the analysis of unpublished data (Perales G, Oliver RJ, Gardiner AS. In Prep). This readme will be updated with the published manuscript when available. Please cite this manuscript if you use this program for your own peer reviewed manuscripts.

##Arguments

**-p, --path**

Corresponds to the input directory where your *.tif files are located. Defaults to the current working directory that this program is run from. Currently only supports .tif formats normalized 0-255.

**-d, --dthresh**
Threshold value for inclusion as a positive dextran (red channel) pixel. Must be an integer between 0-255.

**-v, -vthresh**
Threshold value for inclusion as a positive vessel (green channel) pixel. Must be an integer between 0-255.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

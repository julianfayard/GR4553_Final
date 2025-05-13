Undergraduate Group 1 Final Project GR-4553

Project Overview:
This project examines the widespread flooding in Western North Carolina associated with Hurricane Helene. Just before Helene arrived, a synoptically driven system brought significant rainfall to the region, and the combination of these two events resulted in major flooding. This repository includes radar imagery, upper-air, mid-level charts (300 MB and 700 MB), and Skew-T soundings illustrating the meteorological evolution leading to the event.

Radar Plots and Code:
Python scripts in this directory generate radar base reflectivity plots using NEXRAD data from sites near western North Carolina. These plots illustrate rainfall intensity and the structure of precipitation during the event. Much of the data plotting code was adapted from a template created by Dr. Johna Rudzin at Mississippi State University for GR4553: Computer Methods in Meteorology. To run the code, install and import the following libraries: metpy, cartopy.crs, matplotlib.gridspec, matplotlib.pyplot, numpy, pyart (for radar visualization). Radar data was sourced from Amazon Web Services' open NEXRAD Level II archive. To use a different radar file, replace the filename in the script. For example: f = Level2File('KxxxYYYYMMDD_HHMMSS_V06'). Also, change the title of the plot by editing the string inside the plt.title() function towards the end.

Skew-T Soundings and Code:
Skew-T diagrams were created using upper-air data from the University of Wyoming. These plots show vertical profiles of temperature, dew point, and wind, which helped locate atmospheric instability and moisture depth during Helene. The Skew-T plotting script reads sounding text data and uses 'metpy.plots.Skewt' to generate the diagrams. We modified the file path to different skew-t times to load other soundings.

300mb Wind and Code:
These maps display the geopotential heights and wind speeds at the 300mb level. They show the upper-level jet and divergence pattern in the jet streaks that enhanced lift across the region.
We retrieved this data by downloading from the NSF NCAR Research Data Archive in GRIB or NetCDF format. The Python scripts plot contours of height and color-filled wind speed. You can then replace the input file path to look at different times or levels.
 
700mb RH and Code:
These plots show relative humidity and wind vectors at 700mb, highlighting areas of deep-layer moisture and mid-level flow, which were both crucial for understanding rainfall rates and duration. These scripts follow a similar structure to the 300mb maps. Adjust file paths to retrieve different timestamps.

Gif Image:
The GIFs provided are assembled from the PNGs that were produced by the code, which were then converted into a GIF image by a 3rd party software supplied on ezgif.com.

# 700mb Code (Connor)

#Import Statements

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cf
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from metpy.units import units
from numpy import *
import netCDF4
import metpy.calc as mpcalc
import metpy.constants as mpconst
import matplotlib.gridspec as gridspec
from metpy.plots import add_metpy_logo
from metpy.cbook import get_test_data
from metpy.io import Level2File
import csv
import pygrib
import geopandas

#Plot for the 23rd of September at 00z

#Open File

grbGFS4 = pygrib.open("gfs_4_20240923_0000_000.grb2")

##Find geopotential height and relative humidity values at the 700mb level in the file
hgt700 = grbGFS4.select(name = 'Geopotential Height', level = 700)[0]
rh700 = grbGFS4.select(name = 'Relative humidity', level = 700)[0]
# Find the u and v component of the wind
ucomp700 = grbGFS4.select(name='U component of wind', level=700)[0]
vcomp700 = grbGFS4.select(name='V component of wind', level=700)[0]


uval = ucomp700.values
vval = vcomp700.values

# Establish Windspeed
wspd = np.sqrt(uval**2 + vval**2) * 1.94384

##Define arrays for latitude and longitude
[lats,lons] = hgt700.latlons()


spaces = 40
row_indices = np.arange(0, lats.shape[0], spaces)
column_indices = np.arange(0, lats.shape[1], spaces)

latsub = []
lonsub = []

usub = []
vsub = []

for i in row_indices:
    for j in column_indices:
        latsub.append(lats[i, j])
        lonsub.append(lons[i, j])
        usub.append(uval[i, j])
        vsub.append(vval[i, j])
latsub = np.array(latsub)
lonsub = np.array(lonsub)
usub = np.array(usub)
vsub = np.array(vsub)

##Define lists for height and RH values, while converting height values to dm
hgtval = hgt700.values*0.1
rhval = rh700.values

##Create the figure and projection
fig = plt.figure (figsize=(8,8))
proj=ccrs.LambertConformal(central_longitude=-96.,central_latitude=40.,standard_parallels=(40.,40.))
ax=plt.axes(projection=proj)

##Add a map of the US
ax.set_extent([-125.,-70.,20.,60.])
ax.add_feature(cf.LAND,color='white')
ax.add_feature(cf.OCEAN,color='lightblue')
ax.add_feature(cf.COASTLINE,edgecolor='saddlebrown')
ax.add_feature(cf.STATES,edgecolor='saddlebrown')
ax.add_feature(cf.BORDERS,edgecolor='saddlebrown',linestyle='-')
ax.add_feature(cf.LAKES, alpha=0.5, color='lightblue')

levels = [30, 40, 50, 60, 80, 100, 125, 150, 200]


##Plot wind barbs
plt.barbs(lonsub, latsub, usub, vsub, length=5, transform=ccrs.PlateCarree())

##Plot solid contours for height values
c=plt.contour (lons, lats, hgtval, np.arange(np.min(hgtval),np.max(hgtval),4), linestyles = 'solid', colors = 'black',transform=ccrs.PlateCarree())

##Plot filled contours for RH values, adding a color bar underneath the figure
c2=plt.contourf(lons,lats,rhval,np.arange(70,101,5), cmap='Greens',transform=ccrs.PlateCarree())
cbar = plt.colorbar (location='bottom')
cbar.set_label ('percent')

##Titling the plot
plt.title ('700mb Heights (dm)/ 700mb Relative Humidity (9/23 at 00z)')

# Save the plot as a PNG image
plt.savefig('GFS092300.png')

#Display the plot in view window
plt.show()

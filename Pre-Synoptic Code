# 300 mb Charts Code (Will)

## The following code creates 300mb charts with geopotential heights (dm) and wind (knots), plus wind barbs
## It can be rerun exactly as is using the imports below. The only thing that must be changed is the file name to your NAM Grib2 file of choice.
### In my case, I used data requested from the NSF NCAR Research Data Archive.
## The name of the outfile may also be changed to your name of choice.


"""
Created on Fri May  9 15:41:10 2025

@author: Will
"""

# FINAL PROJECT

# IMPORTS

import numpy as np
import matplotlib.pyplot as plt
import pygrib
import cartopy.crs as ccrs
import cartopy.feature as cf

# Load GRIB2 file
infile = '20240928.nam.t00z.awphys00.tm00.grib2.bratton792895'
grb = pygrib.open(infile)

# Extract 300 mb variables using the correct message index (1-based)
geoh300 = grb[1]  # Geopotential height (300 mb)
u300 = grb[2]     # U component of wind (300 mb)
v300 = grb[3]     # V component of wind (300 mb)

# Extract values and coordinates
hvals = geoh300.values / 10.0  # convert to decameters
uvals = u300.values
vvals = v300.values
wspd = np.sqrt(uvals**2 + vvals**2) * 1.94384  # convert m/s to knots
lats, lons = geoh300.latlons()

# Downsample wind barbs for clarity
spacing = 40
row_indices = np.arange(0, lats.shape[0], spacing)
column_indices = np.arange(0, lats.shape[1], spacing)
lat_sub = []
lon_sub = []
u_sub = []
v_sub = []
for i in row_indices:
    for j in column_indices:
        lat_sub.append(lats[i, j])
        lon_sub.append(lons[i, j])
        u_sub.append(uvals[i, j])
        v_sub.append(vvals[i, j])
lat_sub = np.array(lat_sub)
lon_sub = np.array(lon_sub)
u_sub = np.array(u_sub)
v_sub = np.array(v_sub)

# Set up projection and map
fig = plt.figure(figsize=(8, 8))
proj = ccrs.LambertConformal(central_longitude=-96., central_latitude=40., standard_parallels=(40., 40.))
ax = plt.axes(projection=proj)
ax.set_extent([-125., -70., 20., 60.], crs=ccrs.PlateCarree())
ax.add_feature(cf.STATES, edgecolor='gray')
ax.add_feature(cf.BORDERS, edgecolor='gray')
ax.add_feature(cf.LAKES, alpha=0.4)
ax.add_feature(cf.LAND, color='wheat')
ax.add_feature(cf.OCEAN)

# Plot isotachs (wind speed)
levels = [30, 40, 50, 60, 80, 100, 125, 150, 200]
cf_plot = ax.contourf(lons, lats, wspd, levels=levels, cmap='hot_r', transform=ccrs.PlateCarree())
plt.colorbar(cf_plot, orientation='horizontal', label='Wind Speed (knots)')

# Plot geopotential height contours
hcont = ax.contour(lons, lats, hvals, levels=np.arange(840, 1320, 6), colors='black', linewidths=1.5, transform=ccrs.PlateCarree())
ax.clabel(hcont, inline=True, fontsize=9, fmt='%d')

# Plot wind barbs
ax.barbs(lon_sub, lat_sub, u_sub, v_sub, length=5, transform=ccrs.PlateCarree())

# Title
plt.title('300 mb Geopotential Heights (dm), Isotachs (knots), and Wind Barbs')

# Show plot
plt.savefig('FinalProjectBratton_300mb_20240928_t00z')

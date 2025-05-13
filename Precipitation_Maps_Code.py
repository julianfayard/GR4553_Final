# Total Precipitation Data (Maddie)
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

# Open dataset
precipDataset = netCDF4.Dataset("precip.2024.nc", "r")

# This shouldn't be needed since netCDF4 should auto mask data according to the fill value
# precipDataset.set_auto_mask(True)

# Extract variables / data from dataset
time_var = precipDataset.variables["time"]
time = time_var[:]

precip = precipDataset.variables["precip"][:]
lat = precipDataset.variables["lat"][:]
lon = precipDataset.variables["lon"][:]

# There's a reason, but the lon is shifted by 0.25deg (0.25 - 359.75), but still in a resolution of 0.5deg
# We need to convert 0-360 deg format to -180-180 deg format to make cartopy happy
lon = np.where(lon > 180, lon - 360, lon)

# Times are internally represented as numbers.
# Data loaded represents the 366 days in 2024 (leap year!)
preHeleneDays = (263, 269) # Sept. 20th - 26th
postHeleneDays = (270, 275) # Sept. 27th - Oct. 2nd
totalHeleneDays = (263, 275) # Sept. 20th - Oct. 2nd

# Trim and sum data from specific time ranges
# Data is converted from mm to inches
preHeleneData = np.sum(precip[preHeleneDays[0]:preHeleneDays[1], :, :], axis=0) / 25.4
postHeleneData = np.sum(precip[postHeleneDays[0]:postHeleneDays[1], :, :], axis=0) / 25.4
totalHeleneData = np.sum(precip[totalHeleneDays[0]:totalHeleneDays[1], :, :], axis=0) / 25.4

# Take the bounding box (coordinates) of the area we want
lat_min, lat_max = 33, 37.5
lon_min, lon_max = -85.75, -73.75

# Convert lat/lon to a MeshGrid (lat/lon swapped to conform to correct data shape)
lon, lat = np.meshgrid(lon, lat)

# Create figure and title
fig = plt.figure(figsize=(11, 7), layout="tight")
# fig.suptitle("Precipitation around Hurricane Helene")

# Create grid spec with a 2 row x 2 column grid
gs = fig.add_gridspec(2, 2)

# Create top plot
ax1 = fig.add_subplot(gs[0, :], projection=ccrs.PlateCarree())
ax1.set_title(f"Total Precipitation ({netCDF4.num2date(time[totalHeleneDays[0]], time_var.units).strftime('%b %d')} - {netCDF4.num2date(time[totalHeleneDays[1]], time_var.units).strftime('%b %d')})")

ax1Contour = ax1.contourf(
    lon, lat, totalHeleneData,
    levels=np.linspace(0, 15),
    transform=ccrs.PlateCarree(),
    cmap="viridis"
)

fig.colorbar(ax1Contour, ax=ax1, ticks=np.linspace(0, 15, 7), label="Precipitation (in)", orientation="horizontal", pad=0.025, shrink=0.565)

# Create bottom left plot
ax2 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree())
ax2.set_title(f"Before Helene ({netCDF4.num2date(time[preHeleneDays[0]], time_var.units).strftime('%b %d')} - {netCDF4.num2date(time[preHeleneDays[1]], time_var.units).strftime('%b %d')})")

ax2Contour = ax2.contourf(
    lon, lat, preHeleneData,
    levels=np.linspace(0, 15),
    transform=ccrs.PlateCarree(),
    cmap="viridis"
)

fig.colorbar(ax2Contour, ax=ax2, ticks=np.linspace(0, 15, 7), label="Precipitation (in)", orientation="horizontal", pad=0.025)


# Create bottom right plot
ax3 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree())
ax3.set_title(f"After Helene ({netCDF4.num2date(time[postHeleneDays[0]], time_var.units).strftime('%b %d')} - {netCDF4.num2date(time[postHeleneDays[1]], time_var.units).strftime('%b %d')})")

ax3Contour = ax3.contourf(
    lon, lat, postHeleneData,
    levels=np.linspace(0, 15),
    transform=ccrs.PlateCarree(),
    cmap="viridis"
)

fig.colorbar(ax3Contour, ax=ax3, ticks=np.linspace(0, 15, 7), label="Precipitation (in)", orientation="horizontal", pad=0.025)


# Set shared properties (extent, features, etc.)
for ax in [ax1, ax2, ax3]:
    # Set extent (zoom in)
    # We might want to adjust this on the top map since the aspect ratio will be off
    ax.set_extent(extents=[lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # Add feature(s)
    ax.add_feature(cf.LAND, color="khaki")
    # ax.add_feature(cf.OCEAN, color="lightblue")
    ax.add_feature(cf.STATES, edgecolor="black", linewidth=1)

    # Add our city name/dot on the map (Asheville, NC)
    city_lon, city_lat = -82.5461, 35.5975
    ax.plot(city_lon, city_lat, marker="o", color="black", markersize=3, transform=ccrs.PlateCarree())
    ax.text(
        city_lon + 0.25, city_lat + 0.1,
        "Asheville",
        transform=ccrs.PlateCarree(),
        fontsize=8,
        fontweight="bold",
        ha="center",
        va="bottom",
        color="black"
    )

# Save map image
fig.savefig("map1.png")

# Close file handle
precipDataset.close()
message.txt

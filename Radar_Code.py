# Radar Code (Olivia)
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cf

from metpy.calc import azimuth_range_to_lat_lon
from metpy.cbook import get_test_data
from metpy.io import Level2File
from metpy.plots import add_metpy_logo, add_timestamp, USCOUNTIES
from metpy.units import units

# open file
f = Level2File('KGSP20240927_052216_V06')
print(f.sweeps[0][0])

# pull data
sweep = 0

# in ray first item is header and has azimuth angle
az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])

# take the single azimuth (nominally a mid-point) from data and convert it to azimuth of the boundary between rays of data
diff = np.diff(az)
crossed = diff < -180
diff[crossed] += 360.
avg_spacing = diff.mean()

# Convert mid-point to edge
az = (az[:-1] + az[1:]) / 2
az[crossed] += 180.

# Concatenate with overall start and end of data we calculate using the average spacing
az = np.concatenate(([az[0] - avg_spacing], az, [az[-1] + avg_spacing]))
az = units.Quantity(az, 'degrees')

# calculate ranges for the gates from the metadata

# 5th item is a dict mapping a var name (byte string) to a tuple of (header, data array)
ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
ref_range = (np.arange(ref_hdr.num_gates + 1) - 0.5) * ref_hdr.gate_width + ref_hdr.first_gate
ref_range = units.Quantity(ref_range, 'kilometers')
ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])

rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
rho_range = units.Quantity(rho_range, 'kilometers')
rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])

# extract central lon and lat from file
cent_lon = f.sweeps[0][0][1].lon
cent_lat = f.sweeps[0][0][1].lat

#spec=gridspec.GridSpec(1, 2)
spec = gridspec.GridSpec(1, 1)
#fig = plt.figure(figsize=(15, 8))
fig = plt.figure(figsize=(8,8))

for var_data, var_range, ax_rect in zip((ref, rho), (ref_range, rho_range), spec):
    # Turn into an array, then mask
    data = np.ma.array(var_data)
    data[np.isnan(data)] = np.ma.masked

    # Convert az,range to x,y
    xlocs, ylocs = azimuth_range_to_lat_lon(az, var_range, cent_lon, cent_lat)

    # Plot the data
    crs = ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=cent_lat)
    ax = fig.add_subplot(ax_rect, projection=crs)
    ax.add_feature(USCOUNTIES, linewidth=0.3, edgecolor='gray')
    ax.add_feature(cf.OCEAN, facecolor= 'cyan')
    ax.add_feature(cf.LAND, facecolor= 'tan')
    ax.add_feature(cf.STATES, linewidth=0.6, edgecolor= 'black')
    ax.pcolormesh(xlocs, ylocs, data, cmap='Spectral_r', transform=ccrs.PlateCarree())
    ax.set_extent([cent_lon - 3, cent_lon + 3, cent_lat - 3, cent_lat + 3])
    ax.set_aspect('equal', 'datalim')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='grey', alpha=0.5, linestyle='--')

    ttl = plt.title("KGSP - GREER, SC Radar, 5:30Z, Sep 27 2024")

plt.savefig('radargreer530z.png')
plt.show()

# Skew-T Code (Julian)
from datetime import datetime
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units
from metpy.calc import parcel_profile, cape_cin
import numpy as np
from siphon.simplewebservice.wyoming import WyomingUpperAir

# Set time and station
dt = datetime(2024, 9, 20, 12)
station = 'RNK'

# Request data
df = WyomingUpperAir.request_data(dt, station)

# Remove rows with any missing data
df = df.dropna(subset=['pressure', 'temperature', 'dewpoint', 'u_wind', 'v_wind'])

# Extract variables with units
p = df['pressure'].values * units.hPa
T = df['temperature'].values * units.degC
Td = df['dewpoint'].values * units.degC
u = df['u_wind'].values * units.knots
v = df['v_wind'].values * units.knots

# Compute parcel profile from surface
parcel_trace = parcel_profile(p, T[0], Td[0])

# Compute CAPE/CIN
cape, cin = cape_cin(p, T, Td, parcel_trace)

# Make plot
fig = plt.figure(figsize=(9, 11))
skew = SkewT(fig, rotation=45)

# Plot T, Td, winds, and parcel
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot(p, parcel_trace, 'k', linewidth=2)
skew.plot_barbs(p[::3], u[::3], v[::3])
skew.shade_cape(p, T, parcel_trace)
skew.shade_cin(p, T, parcel_trace)

# Set limits and dry/moist adiabats
skew.ax.set_xlim(-30, 40)
skew.ax.set_ylim(1020, 100)
skew.plot_dry_adiabats(alpha=0.25, color='orangered')
skew.plot_moist_adiabats(alpha=0.25, color='tab:green')

# Titles and CAPE/CIN output
plt.title('{} Sounding'.format(station), loc='left')
plt.title('Valid Time: {}'.format(dt), loc='right')

# Save and show
plt.savefig('20_12z_RNK_sounding.png')
plt.show()
plt.close()

# Used this code to create Skew-T images for 00z and 12z times from September 21 to September 29 2024.

from herbie import Herbie
from toolbox import EasyMap, pc
from paint.standard2 import cm_wind
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib import colormaps

# Herbie object for the HRRR model 6-hr surface forecast product
# H = Herbie('2024-06-25 12:00',
#            model='hrrr',
#            product='subh',
#            fxx=46)

# Download the full GRIB2 file
# H.download()

# Read subset with xarray, like 2-m temperature.

hour = 26
H = Herbie("2024-06-26 00:00", model="nam", fxx=hour)
href = H.xarray(":LTNG:")
print(href)
ax = EasyMap("50m", crs=href.herbie.crs, figsize=[10, 8]).STATES().ax
vmin = 0.1
norm = mpl.colors.Normalize(vmin=vmin, vmax=10)
# kw = cm_wind(units="mph").cmap_kwargs
# kw["norm"] = norm
# kw["cmap"].set_under("white")
cmap = colormaps["YlOrBr"]
cmap.set_under("white")
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    href.ltng,
    transform=pc,
    vmin=0.01,
    vmax=30,
    cmap=cmap
)
plt.colorbar(
    p,
    ax=ax,
    orientation="vertical",
    pad=0.01,
    shrink=0.8
)

ax.set_title(
    f"{href.model.upper()}: Lightning Density\nValid: {href.valid_time.dt.strftime('%H:%M UTC %d %b %Y').item()}",
    loc="left",
)


ax.set_title(href.ltng.GRIB_name, loc="right")
ax.set_extent([-74.5, -71.5, 40, 42])
plt.savefig("6-25-2024[12z](lightning)" + str(hour) + ".png")

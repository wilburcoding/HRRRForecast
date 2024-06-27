from herbie import Herbie
from toolbox import EasyMap, pc
from paint.standard2 import cm_wind
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# Herbie object for the HRRR model 6-hr surface forecast product
# H = Herbie('2024-06-25 12:00',
#            model='hrrr',
#            product='subh',
#            fxx=46)

# Download the full GRIB2 file
# H.download()

# Read subset with xarray, like 2-m temperature.

hour = 25
H = Herbie("2024-06-26 00:00",model="nam", fxx=hour)
href = H.xarray(":GUST:")
print(href)
ax = EasyMap("50m", crs=href.herbie.crs, figsize=[10, 8]).STATES().ax
vmin = 0.1
norm = mpl.colors.Normalize(vmin=vmin, vmax=80)
kw = cm_wind(units="mph").cmap_kwargs
kw["norm"] = norm
kw["cmap"].set_under("white")
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    href.gust * 2.23694,
    transform=pc,
    **kw
)
plt.colorbar(
    p,
    ax=ax,
    orientation="vertical",
    pad=0.01,
    shrink=0.8,
    **cm_wind(units="mph").cbar_kwargs
)

ax.set_title(
    f"{href.model.upper()}: Reflectivity\nValid: {href.valid_time.dt.strftime('%H:%M UTC %d %b %Y').item()}",
    loc="left",
)


ax.set_title(href.gust.GRIB_name, loc="right")
ax.set_extent([-74.5, -71.5, 40, 42])
plt.savefig("6-25-2024[12z](gust)" + str(hour) + ".png")

from herbie import Herbie
from toolbox import EasyMap, pc
from paint.radar2 import cm_reflectivity
import pytz
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
import cartopy.crs as ccrs
est = pytz.timezone('US/Eastern')

hour = 32
H = Herbie("2024-06-29 12:00",model="hrrr", fxx=hour)
href = H.xarray(":REFC:")
ax = EasyMap("50m", crs=href.herbie.crs, figsize=[8.5, 8]).STATES().ax
vmin = 0.1
norm = mpl.colors.Normalize(vmin=vmin, vmax=80)
kw = cm_reflectivity().cmap_kwargs
kw["norm"] = norm
kw["cmap"].set_under("white")
print(href.refc.rolling())
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    href.refc,
    transform=pc,
    **kw
)
plt.colorbar(
    p,
    ax=ax,
    orientation="vertical",
    pad=0.01,
    shrink=0.8,
    **cm_reflectivity().cbar_kwargs
)
ti = str(href.valid_time.dt.strftime("%Y-%m-%dT%H:%M:%S").item())
valid = datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
valid = pytz.utc.localize(valid)
ax.set_title(
    f"{href.model.upper()}: {href.refc.GRIB_name}\nValid: {valid.astimezone(est).strftime('%I:%M %p EST - %d %b %Y')}",
    loc="left",
)
ax.set_title(
    f"Hour: {str(hour)}\nInit: " + href.time.dt.strftime('%Hz - %d %b %Y').item(), loc="right")
ax.set_extent([-74.5, -71.5, 40, 42])
plt.tight_layout()
plt.savefig("rmaintest" + str(hour) + ".png", bbox_inches='tight')

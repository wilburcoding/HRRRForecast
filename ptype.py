from herbie import Herbie
from toolbox import EasyMap, pc
from paint.radar2 import cm_reflectivity
import pytz
import metpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import cartopy.crs as ccrs
est = pytz.timezone('US/Eastern')

hour = 8
# "2020-12-17 6:00
#SNOW
H = Herbie("2022-11-18 12:00", model="hrrr", fxx=hour)
href = H.xarray("(?::CSNOW:|:PRATE:|:CRAIN:|:CICEP:|:CFRZR:)")
ax = EasyMap("50m", crs=href.herbie.crs, figsize=[8.5, 8]).STATES().ax
vmin = 0.1
ptnorm = mpl.colors.Normalize(vmin=0.001, vmax=1.0)
blues = [[136, 148, 223], [101, 116, 211], [
    68, 85, 192], [45, 62, 173], [22, 40, 148], [10, 26, 127], [3, 15, 91]]
for i in range(len(blues)):
  blues[i] = [x/255 for x in blues[i]]
swcmap = mpl.colors.ListedColormap(blues)


kw = cm_reflectivity().cmap_kwargs
kw["norm"] = mpl.colors.Normalize(vmin=0.001, vmax=0.4)
kw["cmap"] = swcmap
kw["cmap"].set_under("white")
location = "Roslyn, NY"
loc = (40.7998, -73.6510)
points = pd.DataFrame(
    {
        "latitude": [loc[0]],
        "longitude": [loc[1]],
        "stid": ["Roslyn"],
    }
)
sm = metpy.calc.smooth_gaussian((href.prate * 3600.0 / 25.4) * href.csnow, 6)
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    sm,
    transform=pc,
    **kw
)
#RAIN
vmin = 0.1
ptnorm = mpl.colors.Normalize(vmin=0.001, vmax=1.0)
greens = [[108, 203, 125], [76, 190, 97], [
    52, 171, 73], [30, 153, 53], [14, 126, 35], [5, 93, 21], [2, 70, 15]]
for i in range(len(greens)):
  greens[i] = [x/255 for x in greens[i]]
racmap = mpl.colors.ListedColormap(greens)
kw = cm_reflectivity().cmap_kwargs
kw["norm"] = ptnorm
kw["cmap"] = racmap
kw["cmap"].set_under("white", alpha=0)
sm = metpy.calc.smooth_gaussian((href.prate * 3600.0 / 25.4) * href.crain, 6)
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    sm,
    transform=pc,
    **kw
)
# SLEET
vmin = 0.1
purples = [[187, 131, 230], [164, 95, 218], [
    151, 73, 213], [135, 51, 200], [120, 35, 187], [105, 18, 174], [83, 7, 142]]
for i in range(len(purples)):
  purples[i] = [x/255 for x in purples[i]]
iccmap = mpl.colors.ListedColormap(purples)
kw = cm_reflectivity().cmap_kwargs
kw["norm"] = mpl.colors.Normalize(vmin=0.001, vmax=0.5)
kw["cmap"] = iccmap
kw["cmap"].set_under("white", alpha=0)
sm = metpy.calc.smooth_gaussian((href.prate * 3600.0 / 25.4) * href.cicep, 6)
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    sm,
    transform=pc,
    **kw
)
ti = str(href.valid_time.dt.strftime("%Y-%m-%dT%H:%M:%S").item())
valid = datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
valid = pytz.utc.localize(valid)
# FRZR
vmin = 0.1
pinks = [[231, 137, 221], [227, 103, 214], [
    216, 71, 200], [196, 36, 179], [174, 21, 158], [154, 13, 139], [128, 6, 115]]
for i in range(len(pinks)):
  pinks[i] = [x/255 for x in pinks[i]]
frcmap = mpl.colors.ListedColormap(pinks)
kw = cm_reflectivity().cmap_kwargs
kw["norm"] = mpl.colors.Normalize(vmin=0.001, vmax=0.8)
kw["cmap"] = frcmap
kw["cmap"].set_under("white", alpha=0)
sm = metpy.calc.smooth_gaussian((href.prate * 3600.0 / 25.4) * href.cfrzr, 6)
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    sm,
    transform=pc,
    **kw
)
ti = str(href.valid_time.dt.strftime("%Y-%m-%dT%H:%M:%S").item())
valid = datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
valid = pytz.utc.localize(valid)
ax.set_title(
    f"{href.model.upper()}: {href.prate.GRIB_name}\nValid: {valid.astimezone(est).strftime('%I:%M %p EST - %d %b %Y')}",
    loc="left",
)
ax.set_title(
    f"Hour: {str(hour)}\nInit: " + href.time.dt.strftime('%Hz - %d %b %Y').item(), loc="right")
# [-75.5, -70.5, 39, 43]
ax.set_extent([-79.8, -77.8, 41, 43])
plt.tight_layout()
plt.savefig("output/" + str(hour) + ".png", bbox_inches='tight')

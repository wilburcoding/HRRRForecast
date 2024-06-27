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

hour = 30
H = Herbie("2024-06-25 18:00", fxx=hour)
href = H.xarray(":CAPE:surface")
print(href)
ax = EasyMap("50m", crs=href.herbie.crs, figsize=[10, 8]).STATES().ax
vmin = 0.1
norm = mpl.colors.Normalize(vmin=vmin, vmax=10000)
# kw = cm_wind(units="mph").cmap_kwargs
# kw["norm"] = norm
# kw["cmap"].set_under("white")
rgbc = [[212, 212, 212], [186, 186, 186], [150, 150, 150], [115, 115, 115], [77, 77, 77], [59, 59, 59]]
rgbc2 = []
lims = [[[135, 195, 255], [0, 43, 87]], [
    [255, 210, 156], [173, 101, 14]], [[251, 255, 145], [205, 212, 21]], [[166, 255, 167], [6, 207, 8]], [[215, 156, 255], [118, 17, 186]]]
bounds = [100, 200, 400, 600, 800,
          1000]
l = 1000
for item in lims:
  up = item[0]
  bo = item[1]
  d1 = (bo[0] - up[0])/7.0
  d2 = (bo[1] - up[1])/7.0
  d3 = (bo[2] - up[2])/7.0
  for i in range(7):
    rgbc.append([up[0] +d1*i, up[1] +d2*i, up[2] +d3*i])
  for i in range(5):
    l += 200
    bounds.append(l)

l+=200
bounds.append(l)
rgbc.append([255, 122, 244])  # Upper bound
for item in rgbc:
  for i in range(3):
    rgbc2.append([item[0]/255.0, item[1]/255.0, item[2]/255.0]) 
cmap = mpl.colors.ListedColormap(rgbc2)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cmap.set_under("white")
p = ax.pcolormesh(
    href.longitude,
    href.latitude,
    href.cape,
    transform=pc,
    cmap=cmap,
    norm = norm
)
plt.colorbar(
    p,
    ax=ax,
    orientation="vertical",
    pad=0.01,
    shrink=0.8
)

ax.set_title(
    f"{href.model.upper()}: SBCAPE\nValid: {href.valid_time.dt.strftime('%H:%M UTC %d %b %Y').item()}",
    loc="left",
)


ax.set_title(href.cape.GRIB_name, loc="right")
ax.set_extent([-74.5, -71.5, 40, 42])
plt.savefig("6-25-2024[12z](cape)" + str(hour) + ".png")

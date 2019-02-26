# Python standard lib geographiclib
import geopy
import geopy.distance
from geographiclib.geodesic import Geodesic
from shapely.geometry import Point, Polygon
import geopandas

coordinates_polygon = [[-33.982909978983756, 151.2465560781668],[-33.98303452845496, 151.24681357023223],[-33.98315018137193, 151.24674383279785],[-33.983021183877476, 151.24648634073242]]

xs, ys = [], []
for i in coordinates_polygon:
    xs.append(i[1])
    ys.append(i[0])

coordinates_rectangle = [[min(xs), max(ys)],[max(xs), max(ys)],[max(xs), min(ys)], [min(xs), min(ys)]]

# Crop Database (in meters)
crop_x = 0.5
crop_y = 0.5
row_y = 0.5
crop_center = [crop_x / 2, crop_y / 2]

coordinates_crops = []

# Upper left corner
lat_a = max(ys)
lon_a = min(xs)
# Lower left corner
lat_b = min(ys)
lon_b = min(xs)
# Upper ritght corner
lat_c = max(ys)
lon_c = max(xs)

coords_a = (lat_a, lon_a)
coords_b = (lat_b, lon_b)
coords_c = (lat_c, lon_c)

# Rectangle profile
start = geopy.Point(lat_a, lon_a)
h = geopy.distance.vincenty(coords_a, coords_b).m
w = geopy.distance.vincenty(coords_a, coords_c).m
print(str(h) + ' Meters (Height)')
print(str(w) + ' Meters (Width)')

# The number of crop units placed horizontally and vertically
units_v = h / crop_y
units_h = w / crop_x

# Distance move
EAST = 90
SOUTH = 180

d = geopy.distance.VincentyDistance(meters = crop_center[1])

crop_coordinates = []
crop_coordinates.append(start)

# Vertical coordinates
for n in range(int(units_v - 1)):
    new_coordinate_crop_vertical = d.destination(point=crop_coordinates[n], bearing=SOUTH)
    crop_coordinates.append(new_coordinate_crop_vertical)

# Horizontal coordinates

for i in range(int(units_v * units_h - 1)):
    # if i < units_v - 1
    new_coordinate_crop_horizontal = d.destination(point=crop_coordinates[i], bearing=EAST)
    # else if i > units_v - 1
    #   new_coordinate_crop_horizontal = d.destination(point=crop_coordinates[i], bearing=EAST)
    crop_coordinates.append(new_coordinate_crop_horizontal)

# 0,5,10,15
# 1,6,11,16
# 2,7,12,17
# 3,8,13,18
# 4,9,14,19



print(crop_coordinates)


# https://geographiclib.sourceforge.io/html/classGeographicLib_1_1Geodesic.html#afdca5eb7c37fa2fecf124aecd6c436fd
# Rectangle height
# h = geod.Inverse(lat_a, lon_a, lat_b, lon_b)
# # s12 is a key defined in geographiclib
# height = h['s12']
# print("Rectangle height {:.2f}m".format(height))

# Rectangle width
# w = geod.Inverse(lat_a, lon_a, lat_c, lon_c)
# width = w['s12']
# print("Rectangle width {:.2f}m".format(width))

# coordinates_crops = []

# area_rectangle = (max(xs) - min(xs))*(max(ys) - min(ys))
# units = area_rectangle/((crop_y + row_y)*crop_x)
# print(units)

# ---------------Geopanda--------------
# insert coordinates to _pnt

# insert the coordinates of crops, which are calcuated from
# the coordinates of the rectangle


#  remove this guy
# ', 0.0'


polys = geopandas.GeoSeries({
    'Farm': Polygon([(-33.98297401942945, 151.24662586585862), (-33.98304630257246, 151.24675327078683), (-33.98307632785995, 151.24661647812707)]),
})

coordinates = []

for i in range(int(units_h * units_v - 1)):
    lat = crop_coordinates[i][0]
    lng = crop_coordinates[i][1]
    coordinate = Point(lat, lng)
    coordinates.append(coordinate)

_pnts = coordinates
crop_index = list(range(int(units_v * units_h - 1)))
pnts = geopandas.GeoDataFrame(geometry=_pnts, index=crop_index)
pnts = pnts.assign(**{key: pnts.within(geom) for key, geom in polys.items()})

# How many trues

print(pnts)

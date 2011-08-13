# pyearthquake - Python Earthquake and MODIS utilities
# Copyright (C) 2010 Christian S. Perone
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pyearthquake import httputil

from PIL import Image
from mpl_toolkits.basemap import Basemap
import pylab

import tempfile
import zipfile 
import os
import datetime
import urllib

class BadZipFile(Exception):
   pass

class InvalidSatellite(Exception):
   pass

class InvalidResolution(Exception):
   pass

URL_RAPIDFIRE_SUBSET = "http://rapidfire.sci.gsfc.nasa.gov/subsets/?subset=%s.%s%s.%s.%s.zip" 
URL_METADATA         = "http://rapidfire.sci.gsfc.nasa.gov/subsets/?subset=%s.%s%s.%s.%s.txt"
IMAGE_FILE           = '%s.%s%s.%s.%s.jpg'

RESOLUTIONS = ["250m", "500m", "2km", "1km"]
SATELLITES  = ["terra", "aqua"]

def parse_term(metadata, term):
   start = metadata.find(term + ":") + len(term)+1
   end   = metadata[start:].find("\n")
   val   = float(metadata[start:start+end])
   return val

def get_modis_subset(dt, subset_name, satellite_name="terra", resolution="1km", coastline=True, show=True):
   if satellite_name not in SATELLITES:
      raise InvalidSatellite("Satellite name invalid, use one of %s" % SATELLITES)

   if resolution not in RESOLUTIONS:
      raise InvalidResolution("Resolution not available, use one of %s" % RESOLUTIONS)


   day_of_year = "%03d" % dt.timetuple().tm_yday
   year = str(dt.year)

   tuple_config = (subset_name, year, day_of_year, satellite_name, resolution)
   url = URL_RAPIDFIRE_SUBSET % tuple_config
   image_filename = IMAGE_FILE % tuple_config
   url_metadata = URL_METADATA % tuple_config

   rfile = httputil.RemoteFile(url)
   rfile.update()
   filename = rfile.filename

   try:
      zipf    = zipfile.ZipFile(rfile.filename) 
   except zipfile.BadZipfile:
      raise BadZipFile("Maybe the data is not yet ready on MODIS site !")
      sys.exit(-1)

   tempdir = tempfile.mkdtemp() 

   for name in zipf.namelist():
      data    = zipf.read(name)
      outfile = os.path.join(tempdir, name)
      f       = open(outfile, 'wb')
      f.write(data)
      f.close() 

   zipf.close()

   image_path  = os.path.join(tempdir, image_filename)
   image_modis = Image.open(image_path)

   filein = urllib.urlopen(url_metadata)
   metadata_data = filein.read()
   filein.close()

   ll_lon = parse_term(metadata_data, "LL lon")
   ll_lat = parse_term(metadata_data, "LL lat")
   ur_lon = parse_term(metadata_data, "UR lon")
   ur_lat = parse_term(metadata_data, "UR lat")

   m = Basemap(projection='cyl', llcrnrlat=ll_lat, urcrnrlat=ur_lat,\
               llcrnrlon=ll_lon, urcrnrlon=ur_lon, resolution='i')
   if coastline:
      m.drawcoastlines()
   m.drawmapboundary(fill_color='aqua') 
   m.imshow(image_modis)
   pylab.title("MODIS %s Image for %s on %s (%s res.)" % (satellite_name,
                                                      subset_name, 
                                                      dt.strftime("%d/%m/%Y"), 
                                                      resolution))
   if show: pylab.show()
   return m
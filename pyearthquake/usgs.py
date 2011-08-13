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
import datetime
import email.utils as eut

CATALOGS = {}
CATALOGS["M1+PAST_HOUR"] = "http://earthquake.usgs.gov/earthquakes/catalogs/eqs1hour-M1.txt"
CATALOGS["M1+PAST_DAY"] = "http://earthquake.usgs.gov/earthquakes/catalogs/eqs1day-M1.txt"
CATALOGS["M1+PAST_7DAY"] = "http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M1.txt"

SHAKEMAPS = {}
SHAKEMAPS["INSTUMENTAL_INTENSITY"] = "http://earthquake.usgs.gov/earthquakes/shakemap/global/shake/%s/download/intensity.jpg"
SHAKEMAPS["PEAK_GROUND_ACC"] = "http://earthquake.usgs.gov/earthquakes/shakemap/global/shake/%s/download/pga.jpg"
SHAKEMAPS["UNCERTAINTY"] = "http://earthquake.usgs.gov/earthquakes/shakemap/global/shake/%s/download/sd.jpg"
SHAKEMAPS["DECORATED"] = "http://earthquake.usgs.gov/earthquakes/shakemap/global/shake/%s/download/tvmap.jpg"
SHAKEMAPS["BARE"] = "http://earthquake.usgs.gov/earthquakes/shakemap/global/shake/%s/download/tvmap_bare.jpg"

class CatalogNotFound(Exception):
   pass

class ShakemapNotFound(Exception):
   pass

class ShakemapNotAvailable(Exception):
   pass

class USGSCatalog:
   def __init__(self, remote_data):
      self.remote_data = remote_data
      self.data = []
      csvreader = remote_data.get_csv_reader()
      self.header = csvreader.next()
      for row in csvreader:
         self.data.append(dict(zip(self.header, row)))

   def __getitem__(self, key):
      return self.data[key]

   def __iter__(self):
      return iter(self.data)   

   def __len__(self):
      return len(self.data)

   @property   
   def last_updated(self):
      dtstr = self.remote_data.get_info("last-modified")
      #return datetime.datetime(*eut.parsedate(dtstr)[:6])
      return dtstr
        

def retrieve_catalog(catalog_name):
   if catalog_name not in CATALOGS:
      raise CatalogNotFound("Use one of %s catalogs" % CATALOGS.keys())

   remote_data = httputil.CSVRemoteFile(CATALOGS[catalog_name])
   return USGSCatalog(remote_data)

   
def retrieve_shakemap(event, shake_map_type):
   import pylab

   if shake_map_type not in SHAKEMAPS:
      raise ShakemapNotFound("Use one of %s shakemap types" % SHAKEMAPS.keys())

   eqid = event["Eqid"]
   rfile = httputil.RemoteFile(SHAKEMAPS[shake_map_type] % eqid)
   rfile.update()
   
   fhandle = open(rfile.filename, "r")
   head = fhandle.read(300)
   fhandle.close()

   if head.find("File Not Found (404)") >= 0:
      raise ShakemapNotAvailable("Shakemap not available for this event !")

   img = pylab.imread(rfile.filename)
   pylab.imshow(pylab.flipud(img))
   pylab.show()
      

def plot_events(events, map_basemap=None, cmap=None, point_size=30, show=True):
   from mpl_toolkits.basemap import Basemap
   import pylab

   if cmap is None: color_map = pylab.cm.jet
   else:            color_map = cmap

   xlist = [float(e["Lon"]) for e in events]
   ylist = [float(e["Lat"]) for e in events]
   mag   = [float(e["Magnitude"]) for e in events]

   if map_basemap is None:
      m = Basemap(projection='cyl', resolution='l')
      m.drawcoastlines()
      m.drawcountries()
      m.drawmapboundary()
   else:
      m = map_basemap

   m.scatter(xlist, ylist, point_size, c=mag,
             cmap=color_map, marker='o', edgecolors='none',
             zorder=10, alpha=0.75)

   if show: pylab.show()
   return m









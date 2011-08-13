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
import pyearthquake
from setuptools import setup

setup(name='pyearthquake',
      version=pyearthquake.__version__,
      description='Python Earthquake and MODIS utilities',
      author='Christian S. Perone',
      author_email='christian.perone@gmail.com',
      url='http://pyevolve.sourceforge.net/wordpress',
      packages=['pyearthquake'],
      install_requires=["matplotlib >= 0.99.0",
                        "numpy >= 1.3.0", 
                        "PIL >= 1.1.6",
                        "basemap >= 0.99.4"], 
      license = "GPLv2",
      keywords = "python modis usgs earthquake analysis aqua terra satellite"
     )

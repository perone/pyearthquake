import urllib
import csv

class RemoteFile:
   def __init__(self, url):
      self.url = url
      self.info = None
      self.filename = None
      
   def update(self):
      self.filename, self.info = urllib.urlretrieve(self.url)

   def get_info(self, key):
      return self.info[key]

class CSVRemoteFile(RemoteFile):
   def __init__(self, url):
      RemoteFile.__init__(self, url)
      self.update()

   def get_csv_reader(self):
      fhandle = open(self.filename, "r")
      return csv.reader(fhandle)

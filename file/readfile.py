import os
from datetime import datetime

def getList(filename):
   return [line.rstrip('\n') for line in open(filename)]
   
def modification_date(filename):
   t = os.path.getmtime(filename)
   return datetime.fromtimestamp(t)
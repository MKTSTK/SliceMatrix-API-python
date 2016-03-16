import pandas as pd
import numpy as np
import json
import urllib
import urllib2
from StringIO import StringIO

class Client(object):
  def __init__(self, apikey):
    self.apikey   = apikey
    self.root_url = "https://api.slicematrix.com/"
    
  # generic HTTPS GET request
  def _make_request(self, url):
    req  = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    data = resp.read()
    return data

  # convert HTTPS GET into JSON
  def _make_json_request(self, url):
    #print url
    data = self._make_request(url)
    #print data
    return json.loads(data)

  # convert HTTPS GET into CSV
  def _make_csv_request(self, url):
    data = self._make_request(url)
    return pd.DataFrame(StringIO(data))

  # returns json of available datasets
  # use these datasets for graph creation
  def get_datasets(self):
    endpoint = self.root_url + "sets?apikey=" + self.apikey
    return self._make_json_request(endpoint)

  # return mst for the designated dataset
  def get_mst(self, dataset, start = None, end = None):#, subset = []):
    endpoint = self.root_url + "mst?apikey=" + self.apikey
    endpoint += "&name=" + dataset['name'] + '_' + dataset['type']
    if start != None:
      start = pd.to_datetime(start).strftime('%Y-%m-%d')
      endpoint += "&start=" + start
    if end != None:
      end = pd.to_datetime(end).strftime('%Y-%m-%d')
      endpoint += "&end=" + end
    # add subset functionality to backend
    #if len(subset) >= 3:
    #  endpoint += "&subset=" + ','.join(subset)
    return self._make_json_request(endpoint)

  # return isomap for the designated dataset    
  def get_isomap(self, dataset, start = None, end = None):
    endpoint = self.root_url + "isomap?apikey=" + self.apikey
    endpoint += "&name=" + dataset['name'] + '_' + dataset['type']
    if start != None:
      start = pd.to_datetime(start).strftime('%Y-%m-%d')
      endpoint += "&start=" + start
    if end != None:
      end = pd.to_datetime(end).strftime('%Y-%m-%d')
      endpoint += "&end=" + end
    return self._make_json_request(endpoint)
    
  # return dataset metadata
  def get_info(self, dataset):
    endpoint = self.root_url + "info?apikey=" + self.apikey
    endpoint += "&name=" + dataset['name'] + '_' + dataset['type']
    return self._make_json_request(endpoint)

  # posts dataframe to db
  def post_tsupload(self, file_name, df):
    endpoint = self.root_url + "tsupload?apikey=" + self.apikey
    print endpoint
    s = StringIO()
    df.to_csv(s)
    file_name = ''.join(e for e in file_name if e.isalnum())
    payload  = {'file-name': file_name,
                'csv-file':  s.getvalue()}
    data = urllib.urlencode(payload)
    print data
    req = urllib2.Request(endpoint, data)
    res = urllib2.urlopen(req)
    status = res.read()
    return status

# endpoints for the following exist
# just need to make client functions
# so... coming soon:

""" 
  # delete old dataset   
  def post_tsdelete(self, dataset):
"""


""" 
  # overwrites old df with new one
  def post_tsupdate(self, df):
"""

""" 
  # append a row(s) to an existing dataframe
  def post_tsappend(self, new_rows):
"""

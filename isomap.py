import SliceMatrix
import pandas as pd
import datetime as dt

auth_token = "YOUR_APIKEY_GOES_HERE"

# create the SliceMatrix API Client

client     = SliceMatrix.Client(auth_token)


# grab all the datasets you have available

datasets   = client.get_datasets()


# pick the dataset you are interested in

dataset    = datasets['graphs'][0]


# get the start and end date of the dataset

info       = client.get_info(dataset)

# use the info to iterate 365 day windows 
# which creep forward 30 days at a time

window_len = 365
creep      = 30

start_date = pd.to_datetime(info['start']) + dt.timedelta(window_len) 
end_date   = pd.to_datetime(info['end'])

isomaps = []
tstamps = []
while start_date <= end_date:
  chunk_start = start_date - dt.timedelta(window_len)
  chunk_end   = start_date
  tstamps.append(chunk_end)
  print chunk_start, chunk_end
  try:
    isomaps.append(client.get_isomap(dataset, start = chunk_start.strftime('%m/%d/%Y'), end = chunk_end.strftime('%m/%d/%Y')))
  except Exception, e:
    print e   
  start_date += dt.timedelta(creep)

# extract some graph invariants (contained within 'meta' tag)
metrix = []
for isomap in isomaps:
  metrix.append(isomap['meta'])

df = pd.DataFrame(metrix, index = tstamps)

print df.head(20)

# save results to a csv

df.to_csv("results_isomap.csv")




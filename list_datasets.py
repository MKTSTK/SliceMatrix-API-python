import SliceMatrix

auth_token = 'insert your auth_token here'

client = SliceMatrix.Client(auth_token)

datasets = client.get_datasets()

for graph in datasets['graphs']:
  print graph



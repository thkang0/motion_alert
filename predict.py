import base64
from googleapiclient import discovery
import json
from oauth2client.client import GoogleCredentials
import re
import sys
from google.oauth2 import service_account


project = "<GCP_project_id>"
model = "<GCP_ML_ENGINE_MODEL>"
version = "<GCP_ML_ENGINE_MODEL_VERSION>"

credentials = service_account.Credentials.from_service_account_file('~/gcp-service-account.json')
ml_service = discovery.build('ml', 'v1', credentials=credentials)

def get_prediction(instance, project, model, version):
  name = 'projects/{}/models/{}'.format(project, model)
  if version:
    name += '/versions/{}'.format(version)
  request_dict = {'instances': [instance]}
  request = ml_service.projects().predict(name=name, body=request_dict)
  return request.execute()  # waits till request is returned

if __name__ == '__main__':

  file_path = sys.argv[1]

  with open(file_path) as ff:
    content = ff.read()

  instance = {'key': '0', 'image_bytes': {'b64': base64.b64encode(content)}}

  result = get_prediction(instance, project,  model, version)

  json_dump_data = json.dumps(result['predictions'])

  json_data = json.loads(json_dump_data)
  son = json_data[0]["scores"][1]

  print int(son*100)

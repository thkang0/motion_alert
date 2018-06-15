import base64
from googleapiclient import discovery
import json
from oauth2client.client import GoogleCredentials
import re
import sys
from google.oauth2 import service_account


project = "tribal-mapper-199302"
model = "thkang0_test"
version = "thkang0_test_201806071740_base"

credentials = service_account.Credentials.from_service_account_file('/home/thkang0/gcp-service-account.json')
#credentials = GoogleCredentials.get_application_default()
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
  #project = sys.argv[2]
  #model = sys.argv[3]
  #version = sys.argv[4] if len(sys.argv) > 4 else ''

  with open(file_path) as ff:
    content = ff.read()

  instance = {'key': '0', 'image_bytes': {'b64': base64.b64encode(content)}}

  result = get_prediction(instance, project,  model, version)

  #json_data = json.loads(result['predictions'][0])
  json_dump_data = json.dumps(result['predictions'])
  #print result['predictions']

  json_data = json.loads(json_dump_data)
  son = json_data[0]["scores"][1]

  print int(son*100)

import os
import sys
import requests
import json

'''
The script sends POST, GET, DELETE requests to the web server
and asks for json content in response.
sample usage is: python test_rest.py --resource_url http://192.168.242.14:80/posts
After executing all the testcase, test summary is printed.
'''

resource_id = 0

def process_result(response, testcase_name):
  if response.status_code / 200 == 1: 
    print testcase_name, ":PASS"
    return True
  else:
    print testcase_name, ":FAIL"
    return False

def test_get_index(base_url):
  accept_hdr = {"Accept": "application/json"}
  response = []
  try:
    response = requests.get(base_url, headers = accept_hdr)
  except requests.exceptions.ConnectionError:
    print "test_get_index :FAIL"
    sys.stderr.write('error connectiong ' + base_url)
    return False
  return process_result(response, "test_get_index")

def test_post_resource(base_url):
  global resource_id
  accept_hdr = {"Accept": "application/json", "Content-Type":"application/json"}
  payload = {"name":"tolkein1","title":"Gollum1","content":"My Precious1"}
  base_url = base_url + ".json"
  response = []
  try:
    response = requests.post(base_url, headers = accept_hdr, data = json.dumps(payload))
  except requests.exceptions.ConnectionError:
    print "test_post_resource: FAIL"
    sys.stderr.write('error connectiong ' + base_url)
    return False
  if response.status_code == 201:
    resource_id = response.json()['id']
  return process_result(response, "test_post_resource")

def test_get_resource(base_url):
  global resource_id
  accept_hdr = {"Accept": "application/json"}
  base_url = base_url + "/" + str(resource_id) + ".json"
  response = []
  try:
    response = requests.get(base_url, headers = accept_hdr)
  except requests.exceptions.ConnectionError:
    print "test_get_resource: FAIL"
    sys.stderr.write('error connectiong ' + base_url)
    return False
  return process_result(response, "test_get_resource")

def test_delete_resource(base_url):
  global resource_id
  accept_hdr = {"Accept": "application/json"}
  base_url = base_url + "/" + str(resource_id) + ".json"
  response = []
  try:
    response = requests.delete(base_url, headers = accept_hdr)
  except requests.exceptions.ConnectionError:
    print "test_delete_resource: FAIL"
    sys.stderr.write('error connectiong ' + base_url)
    return False
  return process_result(response, "test_delete_resource")

def main():
  args = sys.argv[1:]

  if not args or args[0] != "--resource_url":
    print 'usage: --resource_url <url of resource>'
    print 'ex. python test_rest.py --resource_url http://192.168.242.14:80/posts'
    sys.exit(1)

  url = args[1]

  num_passed = 0
  total_tc = 4
  if test_get_index(url):
    num_passed+=1
  if test_post_resource(url):
    num_passed+=1
  if test_get_resource(url):
    num_passed+=1
  if test_delete_resource(url):
    num_passed+=1
  print
  print '########################'
  print 'Num passed testcases:', num_passed
  print 'Num failed testcases:', total_tc - num_passed
  
if __name__ == "__main__":
  main()

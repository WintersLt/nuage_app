#!/usr/bin/env python

import os
import sys
import requests
import json
import logging

'''
The script sends POST, GET, DELETE requests to the web server
and asks for json content in response.
The script also logs the relust to file "test.log"
sample usage is: python test_rest.py --resource_url http://192.168.242.14:80/posts --log DEBUG
After executing all the testcase, test summary is printed.
'''

# create logger with 'spam_application'
logger = logging.getLogger('test_rest')

resource_id = 0

def process_result(response, testcase_name):
  if response.status_code / 200 == 1: 
    logger.info("%s :PASS", testcase_name)
    return True
  else:
    logger.info("%s :FAIL", testcase_name)
    return False

def test_get_index(base_url):
  accept_hdr = {"Accept": "application/json"}
  response = []
  try:
    response = requests.get(base_url, headers = accept_hdr)
  except requests.exceptions.ConnectionError:
    logger.warn("test_delete_resource: FAIL")
    logger.error('error connectiong %s', base_url)
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
    logger.warn("test_delete_resource: FAIL")
    logger.error('error connectiong %s', base_url)
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
    logger.warn("test_delete_resource: FAIL")
    logger.error('error connectiong %s', base_url)
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
    logger.warn("test_delete_resource: FAIL")
    logger.error('error connectiong %s', base_url)
    return False
  return process_result(response, "test_delete_resource")

def main():
  args = sys.argv[1:]

  if not args or args[0] != "--resource_url":
    print 'usage: --resource_url <url of resource> [-log <DEBUG/WARNING/ERROR>]'
    print 'ex. python test_rest.py --resource_url http://192.168.242.14:80/posts -log DEBUG'
    sys.exit(1)

  url = args[1]
  del args[0:2]

  numeric_level = logging.DEBUG
  if (args and args[0] == "--log"):
    loglevel = args[1]
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % loglevel) 

  logger.setLevel(numeric_level)
  # create file handler which logs even debug messages
  fh = logging.FileHandler('test.log')
  fh.setLevel(numeric_level)
  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.ERROR)
  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  # add the handlers to the logger
  logger.addHandler(fh)
  logger.addHandler(ch)


  logger.info('Executing nuage_app tests suite')
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
  
  logger.info('########################')
  logger.info('Number of passed testcases: %d', num_passed)
  logger.info('Number of failed testcases: %d', total_tc - num_passed)
  print '########################'
  print 'Number of passed testcases:', num_passed
  print 'Number of failed testcases:', total_tc - num_passed
  
if __name__ == "__main__":
  main()

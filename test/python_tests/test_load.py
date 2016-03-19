import os
import sys
import time;
import gevent.monkey
gevent.monkey.patch_socket()
from gevent.pool import Pool
import requests
import json

'''
The script sends GET requests to the web server for all the resources
and asks for json content in response.
This performs load testing by using greenlets and gevent module
It sends concurrent requests to the server, prints average time takes for all requests
sample usage is: python test_load.py --resource_url http://192.168.242.14:80/posts --concurrency 50 --num_requests 1000
The above example executes 1000 get requests with concurrency level of 50
'''

resource_id = 0

def process_result(response, testcase_name):
  if response.status_code / 200 == 1: 
    #print testcase_name, ":PASS"
    return True
  else:
    #print testcase_name, ":FAIL"
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

def usage():
   print 'usage: --resource_url <url of resource> --concurrency <num concurrent greenlets> --num_requests <number>'
   print 'ex. python test_load.py --resource_url http://192.168.242.14:80/posts --concurrency 50 --num_requests 1000'
   sys.exit(1)


def main():
  args = sys.argv[1:]
  concurrency = 0
  num_requests = 0

  if not args or args[0] != "--resource_url":
    usage()

  url = args[1]
  del args[0:2]
  if args and args[0] == "--concurrency":
    concurrency = int(args[1])
    del args[0:2]
  else:
    usage()

  if args and args[0] == "--num_requests":
    num_requests = int(args[1])
    del args[0:2]
  else:
    usage()

  pool = Pool(concurrency)
  t1 = time.time()
  for i in range(num_requests):
      pool.spawn(test_get_index, url)
  pool.join()
  t2 = time.time()
  print "Average time: ", (t2-t1)/1000, " seconds"

if __name__ == "__main__":
  main()

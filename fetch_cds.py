#!/usr/bin/env python

import requests
import argparse
from xml.etree import ElementTree
from requests.auth import HTTPDigestAuth

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--user', required=True, help='user name for jgi.doe.gov')
    parser.add_argument('--password', required=True, help='password for jgi.doe.gov')
    args = parser.parse_args()
    return args

def sign_on(args):
    s = requests.session()
    payload = {'login':args.user,'password':args.password}
    signon_page ="https://signon.jgi.doe.gov/signon/create"
    r = s.post(signon_page, data=payload)
    print r.text
    return s

def download_file(url,s):
    local_filename = url.split('/')[-1]
    r = s.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename


def main():
    args = parse_args()
    test_file_url ='http://genome.jgi.doe.gov/PhytozomeV10/download/_JAMO/53112a6949607a1be0055904/Sitalica_164_v2.1.cds_primaryTranscriptOnly.fa.gz'
    s = sign_on(args)
      
    download_file(test_file_url,s)

main()

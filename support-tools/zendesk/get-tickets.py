#!/usr/bin/python

import requests
import getpass
import argparse
import os
import json
import yaml

parser = argparse.ArgumentParser(description='Fetch one or more zendesk tickets')
parser.add_argument('-c', '--config_file', help='config file path')
parser.add_argument('-u', '--user', help='Zendesk username')
parser.add_argument('-e', '--endpoint', help='Zendesk endpoint')
parser.add_argument('-p', '--password', help='Zendesk password')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--tickets', action='append', type=int, help='a Zendesk ticket number')
group.add_argument('-q', '--query', help='Zendesk query string')

args = parser.parse_args()

cfg = {}
if args.config_file and os.path.exists(args.config_file):
    cfg = yaml.load(open(args.config_file).read())

if args.user:
    cfg['user'] = args.user

if args.password:
    cfg['password'] = args.password

if args.endpoint:
    cfg['endpoint'] = args.endpoint

if cfg.get('password') is None:
    cfg['password'] = getpass.getpass()

s = requests.session()
s.auth = (cfg['user'], cfg['password'])

if args.tickets:
    for ticket in args.tickets:
        data1 = s.get('%s/api/v2/tickets/%d.json' % (cfg['endpoint'], ticket)).text
        data2 = s.get('%s/api/v2/tickets/%d/comments.json' % (cfg['endpoint'], ticket)).text
        # Todo: parse and make the output concise
        print json.dumps(json.loads(data1), indent=4)
        print json.dumps(json.loads(data2), indent=4)
else:
    data = json.loads(s.get('%s/api/v2/search.json' % cfg['endpoint'], params={ 'query':  args.query }).text)
    for ticket in data['results']:
        # Todo: parse and make the output concise
        # print json.dumps(ticket, indent=4)
        print ticket['id']
        # data2 = s.get('%s/api/v2/tickets/%d/comments.json' % (cfg['endpoint'], ticket)).text
        # print json.dumps(json.loads(data2), indent=4)

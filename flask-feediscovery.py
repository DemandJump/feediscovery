#####################################################

#####################################################
import sys, re, logging, yaml, os, urllib2
import feedparser, urlparse
import extractlinks
from extractlinks import LinkExtractor

from flask import request, Flask, jsonify, Response
app = Flask(__name__)

import libmc
mc = libmc.Client(['localhost:11211'])

@app.route('/feediscovery', methods = ['GET'])
def mainhandler():
    site_url = request.json['url']
    force = request.json['force'].lower() in ['true','1']
    if site_url:
        feeds = mc.get(site_url)
        if feeds is not None and not force:
            print "Memcache hit."
        else:
            print "Running feediscovery"
            result = urllib2.urlopen(site_url).read()
            parser = LinkExtractor()
            parser.set_base_url(site_url)
            parser.feed(result)
            if parser.links:
                feeds = parser.links
                mc.set(site_url, feeds)
            else:
                feeds = []
    return jsonify(results = feeds)


@app.route('/ping', methods = ['GET'])
def pingfunction():
    return 'alive'

app.debug = True
app.run(host='0.0.0.0')













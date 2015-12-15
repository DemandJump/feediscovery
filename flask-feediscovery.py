#####################################################

#####################################################
import sys, re, logging, yaml, os, urllib2, cookielib
import feedparser, urlparse
import extractlinks
from extractlinks import LinkExtractor
from bs4 import BeautifulSoup

from flask import request, Flask, jsonify, Response
app = Flask(__name__)

import libmc
mc = libmc.Client(['localhost:11211'])

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


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
            result = None
            try:
                req = urllib2.Request(site_url, headers=hdr)
                page = urllib2.urlopen(req)
                result = page.read()
            except urllib2.URLError, e:
                print e.args
            except urllib2.HTTPError, e:
                print e.args

            if result:
                content = BeautifulSoup(result)
                feeds = [v.attrs for v in content.find_all(href=True, rel='alternate', type=re.compile('rss|atom'))]
                if not feeds:
                    # Check feedburner
                    feeds = [v.attrs for v in content.find_all(href=re.compile('feedburner'),rel='nofollow')]

    return jsonify(results = feeds)


@app.route('/ping', methods = ['GET'])
def pingfunction():
    return 'alive'

app.debug = True
app.run(host='0.0.0.0')













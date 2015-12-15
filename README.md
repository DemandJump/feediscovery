feediscovery
======

**feediscovery** is a RESTful API for identifying RSS feeds from a given url powered by Flask. The
service makes use of **memcached** to store previously identified RSS feeds associated with a given url. 

Setup
-----

On a system running **memcached** at 'localhost:11211', with Python 2.7, intialize a virtual environment


```shell
sudo pip install virtualenv
cd pylash
. venv/bin/activate
```

Within the application directory install Python dependencies:

```shell
pip install -r requirements.txt
```

Once complete, the application server can be started as follows:

```shell
python flask-feediscovery.py 
```

This will launch the server at http://localhost:5000 by default. 

Example
-------

```shell
curl -H "Content-type: application/json" -X GET "http://0.0.0.0:5000/feediscovery" -d '{"url":"http://www.homebrewfinds.com","force":"true"}'
```

```json
{
  "results": [
    {
      "href": "http://www.homebrewfinds.com/feed", 
      "rel": "alternate", 
      "title": "Homebrew Finds &raquo; Feed", 
      "type": "application/rss+xml"
    }, 
    {
      "href": "http://www.homebrewfinds.com/comments/feed", 
      "rel": "alternate", 
      "title": "Homebrew Finds &raquo; Comments Feed", 
      "type": "application/rss+xml"
    }
  ]
}
```


# URL shortener
This URL shortened is built using python 3.12 and the FastAPI framework.

## Setting up
### Virtual environment
To setup a virtual environment please run the following commands:
```
virtualenv -p python3.12 .venv
source .venv/bin/activate
```
### Installing dependencies
The dependencies are stored in requirements.txt, please install these 
before attempting to run the app
```
pip install -r requirements.txt
```

## Running the server
To run the server, please run this command:

```
uvicorn  main:app --reload
```

### Shortening URLS
To shorten a given url, you would use the url_shortener endpoint.
An example of calling said endpoint:
```
0.0.0.0:8000/this-is-a-really-long-url-that-needs-to-be-shortened
```
This should return a shortened url to the user.
Example response:
```
{
  "url": "https://short.url/lcaiYqe1"
}
```

### Redirecting to original url
Once you have your shortened url, you can use the redirect_to_longer endpoint.
An example of calling said endpoint:
```
0.0.0:8000/redirect/https://short.url/lcaiYqe1
```

this should redirect you back to:
```
http://0.0.0.0:8000/this-is-a-really-long-url-that-needs-to-be-shortened
```

and return a response that looks like:
```
{
  "message": "You have been redirected to long_url from short_url.",
  "long_url": "0.0.0:8000/this-is-a-really-long-url-that-needs-to-be-shortened",
  "short_url": "https://short.url/GQYWafTb"
}
```

## Running the tests
The tests use pytest and can be run using the following command: 
```
python -m pytest test_main.py
```
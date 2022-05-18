import requests

quote_url = None

def configure_request(app):
    global quote_url
    quote_url = app.config['RANDOM_QUOTE_URL']

def get_random_quote():
    '''
    Function retrieves random quote and passing the JSON as the data intended
    '''
    response = requests.get(quote_url)

    if response.status_code == 200:
        print(response.json())

        return response.json()

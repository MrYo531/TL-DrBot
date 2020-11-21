import requests
import config
from newspaper import Article

def summry(url):
    art = Article(url)
    art.download()
    art.parse()
    text = art.text()

    key = config.API_KEY
    endpoint = "https://api.smmry.com"

    data = {
        "sm_api_input": text,
        "sm_length" : 1
    }
    params = {
        "SM_API_KEY": key,

    }
    header_params = {"Expect":"100-continue"}
    r = requests.post(url=endpoint, params=params, data=data, headers=header_params)

    return r.json()


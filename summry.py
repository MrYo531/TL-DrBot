import requests
import config
from newspaper import Article

def summry(url):
    art = Article(url)
    art.download()
    art.parse()
    text = art.text

    key = config.API_KEY
    endpoint = "https://api.smmry.com"

    data = {
        "sm_api_input": text
    }
    params = {
        "SM_API_KEY": key,
        "SM_LENGTH": 1
    }
    header_params = {"Expect":"100-continue"}
    r = requests.post(url=endpoint, params=params, data=data, headers=header_params).json()

    # TODO: Have a better handling process
    if "sm_api_error" in r:
        return text

    return r["sm_api_content"]



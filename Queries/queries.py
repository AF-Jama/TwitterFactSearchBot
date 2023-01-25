import requests
import os
from dotenv import load_dotenv
import requests_async as request
import time
import openai
from config import config

load_dotenv()

class Query:
    params = {
    "location": "New York, New York, United States",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "api_key": os.environ.get('API_KEY')
    }



    @classmethod
    def search(cls,query):
        '''class method called on className or object,'''
        try:
            cls.params['q'] = query
            r = requests.get(os.environ.get('BASE_URL'),params=cls.params)
            r = r.json()

            time.sleep(8)

            return {
                "engine":r["search_parameters"]["engine"],
                "query":r["search_parameters"]["q"],
                "totalResultDisplayed":r["search_information"]["total_results"],
                "results_text": {
                    "snippet":r["organic_results"][0]["snippet"],
                    "link":r["organic_results"][0]["link"],

                } if len(r["organic_results"])>0 else None,
            } # returns first index of "organic results if array length is greater than 0, using ternary operator"

        except:
            '''triggered if try block triggers error'''
            return None

if __name__ == "__main__":
    Query.search("Will the world end")


import logging

import requests
import json

import image_scraper.constants as constants


def get_image_urls(search_term: str, n: int) -> dict[int, str]:
    page_size = 10

    query_params = {
        "key": constants.IMAGE_API_KEY,
        "cx": constants.IMAGE_API_CX,
        "searchType": "image",
        "q": search_term,
        "start": 1
    }

    urls = {}
    num_processed = 0
    logging.info(f"fetching {n} image urls for search term {search_term}")
    while num_processed < n:
        exit_early = False

        res = requests.get(url="https://www.googleapis.com/customsearch/v1", params=query_params)

        res.raise_for_status()

        res_dict = json.loads(res.text)
        for item in res_dict.get("items", []):
            if "link" in item:
                urls[num_processed] = item["link"]
                num_processed += 1
                if num_processed == n:
                    exit_early = True
                    break

        if exit_early:
            break

        query_params["start"] += page_size

        logging.info(f"num urls fetched: {num_processed}")

    return urls

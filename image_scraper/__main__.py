import os
import argparse
import logging
from queue import Queue
from _queue import Empty
from threading import Thread
import re
from pathlib import Path

import image_scraper.image_api_client as image_api_client
import image_scraper.util as util


logging.basicConfig(level="INFO", format="%(asctime)s %(levelname)-8.8s %(module)-25.25s:%(lineno)-5.5s %(message)s",)


def _process_queue_task(q: Queue, urls: dict[int, str], target_folder: str):
    while True:
        try:
            image_id = q.get(timeout=1)
            url = urls[image_id]
            util.download_image(url, str(image_id), target_folder)
            q.task_done()
        except Empty:
            pass
        except Exception:
            q.task_done()
            logging.exception(f"problem processing queue entry {image_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("query")
    parser.add_argument("n")

    args = parser.parse_args()

    query = args.query
    n = int(args.n)

    if n > 1000000:
        raise ValueError("number of images (n) must be <= 1000000")

    pattern = re.compile(r"\W+")
    folder_name = pattern.sub("", query)
    target_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "downloaded", folder_name)
    if os.path.exists(target_folder):
        raise ValueError(f"results for query {query} are already present on this machine - please migrate the data")

    urls = image_api_client.get_image_urls(query, n)

    Path(target_folder).mkdir(parents=True, exist_ok=True)

    q = Queue()
    [q.put(image_id) for image_id in urls]

    num_workers = 10

    for i in range(0, num_workers):
        thread_name = f"api-poller-{i}"
        Thread(
            target=_process_queue_task,
            name=thread_name,
            kwargs={"q": q, "urls": urls, "target_folder": target_folder},
            daemon=True,
        ).start()

    q.join()

    logging.info("done")

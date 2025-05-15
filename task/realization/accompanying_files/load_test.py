import threading

import time

import urllib.request



URL = "http://localhost:8080/index.php"

NUM_REQUESTS = 1000

CONCURRENCY = 50



success = 0

fail = 0

lock = threading.Lock()



def worker():

    global success, fail

    try:

        with urllib.request.urlopen(URL, timeout=10) as response:

            if response.status == 200:

                with lock:

                    success += 1

            else:

                with lock:

                    fail += 1

    except Exception:

        with lock:

            fail += 1



def run_load():

    threads = []

    start = time.time()



    for i in range(NUM_REQUESTS):

        t = threading.Thread(target=worker)

        threads.append(t)

        t.start()

        while threading.active_count() > CONCURRENCY:

            time.sleep(0.01)



    for t in threads:

        t.join()



    duration = time.time() - start

    print(f"Total requests: {NUM_REQUESTS}")

    print(f"Success: {success}, Fail: {fail}")

    print(f"Time elapsed: {duration:.2f} s")

    print(f"Requests per second: {NUM_REQUESTS/duration:.2f}")

    print(f"Average time per request: {duration*1000/NUM_REQUESTS:.2f} ms")



if __name__ == "__main__":

    run_load()
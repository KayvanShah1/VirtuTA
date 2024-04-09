import json
import sys
import time
import random

from piazza_api import Piazza
from piazza_api.exceptions import RequestError

p = Piazza()
p.user_login()

course = p.network(sys.argv[1])

mapSave = {}

posts = course.iter_all_posts(limit=100000000000)
for post in posts:
    content = post["history"][0]["content"]
    post_id = post["nr"]
    print(post_id)
    mapSave[post_id] = content
    time.sleep(1)
    try:
        with open("DSCI552.json", "w") as f:
            f.write(json.dumps(mapSave))
    except Exception as e:
        print("Error:", e)

print("Data saved successfully!")

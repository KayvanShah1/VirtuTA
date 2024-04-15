import csv
import json
import sys
import time
import random
import re

from piazza_api import Piazza
from piazza_api.exceptions import RequestError

p = Piazza()
p.user_login()
course = p.network("lhjo3qc1jfn1e1")

posts = course.iter_all_posts(limit=100000000000)

# Define column names for the CSV file
fieldnames = ['Post ID', 'Post Created Date','Post Title', 'Folder Name', 'Post Content']

with open("DSCI552.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for post in posts:
        
        post_id = post["nr"]
        post_title = post["history"][0]["subject"]
        folder_name = post["folders"]
        post_created_date=post["history"][0]["created"]
        content = post["history"][0]["content"]
        content = content.replace('\n', ' ')
        post_content = re.sub(r'<[^>]*>', '', content)
        writer.writerow({'Post ID': post_id, 
                         'Post Created Date':post_created_date,
                         'Post Title': post_title,
                         'Folder Name': folder_name, 
                         'Post Content': post_content})

        time.sleep(1)

print("Data saved successfully!")

import csv
import json
import sys
import time
import re

from piazza_api import Piazza


def scraping(course_id, path_to_csv):
    p = Piazza()
    p.user_login()
    course = p.network(course_id)

    posts = course.iter_all_posts(limit=1000)
    fieldnames = ["Post ID", "Post Created Date", "Post Title", "Folder Name", "Post Content", "Child Content"]

    with open(path_to_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for post in posts:

            post_id = post["nr"]
            post_title = post["history"][0]["subject"]
            folder_name = post["folders"]
            post_created_date = post["history"][0]["created"]
            content = post["history"][0]["content"]
            content = content.replace("\n", " ")
            post_content = re.sub(r"<[^>]*>", "", content)
            has_children = bool(post.get("children"))
            child_content_combined = {}
            if has_children:
                children = post["children"]
                for idx, child in enumerate(children, 1):
                    child_content = {}
                    child_content_values = {}
                    child_content_values["type"] = child["type"]
                    child_content_values["content"] = child.get("history", [{}])[0].get("content", "")
                    child_content_values["content"] = re.sub(r"<[^>]*>", "", child_content_values["content"])
                    if not child_content_values["content"]:
                        child_content_values["content"] = child.get("subject", "")
                        child_content_values["content"] = re.sub(r"<[^>]*>", "", child_content_values["content"])

                    child_content[f"Child {idx}"] = child_content_values
                    if child.get("children"):
                        for nested_child_idx, nested_child in enumerate(child["children"], 1):
                            nested_child_content_values = {}
                            nested_child_content_values["type"] = nested_child["type"]
                            nested_child_content_values["content"] = re.sub(
                                r"<[^>]*>", "", nested_child.get("subject", "")
                            )
                            child_content[f"Nested Child {nested_child_idx}"] = nested_child_content_values

                    child_content_combined.update(child_content)

            writer.writerow(
                {
                    "Post ID": post_id,
                    "Post Created Date": post_created_date,
                    "Post Title": post_title,
                    "Folder Name": folder_name,
                    "Post Content": post_content,
                    "Child Content": json.dumps(child_content_combined),
                }
            )

            time.sleep(1)
    print("Data saved successfully!")


scraping(sys.argv[1], sys.argv[2])

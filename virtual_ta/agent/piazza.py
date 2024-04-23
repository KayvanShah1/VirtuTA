from pprint import pformat
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
from piazza_api import Piazza
from settings import PiazzaBotConfig, get_logger


class PiazzaBot:
    def __init__(self, network_id: str, creds: PiazzaBotConfig):
        self.network_id = network_id
        self.piazza = Piazza()
        self.logger = get_logger(name="PiazzaBot")

        # Login to Piazza client
        self.login(creds)

        self.course = self.piazza.network(network_id=network_id)
        self.piazza_rpc = self.piazza._rpc_api

    def login(self, creds: PiazzaBotConfig):
        self.piazza.user_login(email=creds.PIAZZA_USER_EMAIL, password=creds.PIAZZA_USER_PASSWORD)

    def get_unattended_feeds(self):
        response = self.piazza_rpc.request(
            method="network.filter_feed",
            data={"nid": self.network_id, "unresolved": 1},
            api_type="logic",
        )
        if response["result"] is not None:
            return response["result"]["feed"]

        self.logger.error(f"{response['error']}: '{self.network_id}'")
        return {"error": response["error"]}

    def get_post_data(self, post_id: str):
        return self.piazza_rpc.content_get(cid=post_id, nid=self.network_id)

    def parse_s3_url(self, url):
        # Parse the URL
        parsed_url = urlparse(url)

        # Extract the bucket name and prefix from the query string
        query_params = parse_qs(parsed_url.query)
        prefix = query_params.get("prefix")[0]

        piazza_cdn_host = "https://cdn-uploads.piazza.com"

        # Return the parsed components as a dictionary
        return f"{piazza_cdn_host}/{prefix}"

    def parse_answer_data(self, answer_data):
        parsed_answer = {"text": None, "img": []}
        if "history" in answer_data:
            content = BeautifulSoup(answer_data["history"][0]["content"], "lxml")
            parsed_answer["text"] = content.get_text().strip()
            img_tags = content.find_all("img")
            parsed_answer["img"] = [self.parse_s3_url(img.get("src")) for img in img_tags]
        return parsed_answer

    def parse_followup_data(self, followup_data):
        parsed_followup = {"subject": followup_data.get("subject"), "feedback": [], "fid": followup_data.get("uid")}
        if "children" in followup_data:
            for feedback in followup_data["children"]:
                parsed_followup["feedback"].append(feedback.get("subject", ""))
        return parsed_followup

    def parse_post_data(self, data: dict) -> dict:
        parsed_data = {
            "post_id": data.get("nr"),
            "uid": data.get("id"),
            "title": data["history"][0]["subject"].strip(),
            "content_text": "",
            "image_urls": [],
            "answers": {"s_answer": {"text": None, "img": []}, "i_answer": {"text": None, "img": []}, "followup": []},
        }

        # Extract and process content
        content = BeautifulSoup(data["history"][0]["content"], "lxml")
        parsed_data["content_text"] = content.get_text().strip()

        # Extract image URLs
        img_tags = content.find_all("img")
        parsed_data["image_urls"] = [self.parse_s3_url(img.get("src")) for img in img_tags]

        # Extract answers and followups
        children = data.get("children", [])
        for child in children:
            atype = child.get("type")
            if "answer" in atype:
                parsed_data["answers"][atype] = self.parse_answer_data(child)
            elif atype == "followup":
                parsed_data["answers"]["followup"].append(self.parse_followup_data(child))
        return parsed_data

    def create_conversation_thread(self, data: dict):
        thread = {"uid": data["uid"], "conversation": ""}

        conversation = f"""Title: {data["title"]}\n"""
        conversation += f"Content: {data['content_text']}\n\n"

        # Add initial answers
        conversation += "Initial Answers:\n"
        if data["answers"]["i_answer"]["text"]:
            conversation += f"Instructor Answer: {data['answers']['i_answer']['text']}\n"
        if data["answers"]["s_answer"]["text"]:
            conversation += f"Student Answer: {data['answers']['s_answer']['text']}\n"
        conversation += "\n"

        # Add follow-ups and feedback
        conversation += "Follow-ups and Feedback:\n"
        for followup in data["answers"]["followup"]:
            conversation += f"Follow-up: {followup['subject']}\n"
            if followup["feedback"]:
                conversation += "Feedback:\n"
                for feedback in followup["feedback"]:
                    conversation += f"- {feedback}\n"

        thread["conversation"] = conversation

        return thread

    def get_unattended_posts(self):
        feeds = self.get_unattended_feeds()

        for post in feeds:
            resp = self.get_post_data(post_id=post["nr"])
            resp = self.parse_post_data(resp)
            self.logger.info(pformat(resp))
            conv = self.create_conversation_thread(resp)
            self.logger.info(pformat(conv))


if __name__ == "__main__":
    piazza_creds = PiazzaBotConfig()

    bot = PiazzaBot(network_id="lurzv0qdtfm55d", creds=piazza_creds)
    bot.get_unattended_posts()

import os
import xml.etree.ElementTree as ET

import requests
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from jinja2 import Template
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from rich.pretty import pretty_repr
from settings import APIKeys, Path, get_logger
from youtube_transcript_api import YouTubeTranscriptApi

logger = get_logger(__name__)


class Endpoints:
    """
    A class to store the endpoints for the YouTube Data API v3.

    Attributes
    ----------
    BASE_URL : str
        The base URL for the YouTube Data API v3.
    SEARCH : str
        The URL endpoint for the YouTube search API.
    CAPTIONS : str
        The URL endpoint for the YouTube captions API.
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"
    SEARCH = f"{BASE_URL}/search"
    CAPTIONS = f"{BASE_URL}/captions"


class RelatedYouTubeVideos:
    """
    A class to interact with the YouTube Data API v3 for retrieving related videos and captions.

    Attributes
    ----------
    api_key : str
        The API key used for authenticating requests to the YouTube Data API.
    credentials : service_account.Credentials
        The credentials object created from the service account file.
    token : str
        The access token used for authorization.

    Methods
    -------
    get_access_token():
        Refreshes and retrieves the access token.

    make_oauth_request(url: str, params: dict, headers: dict = None)
        Makes an authenticated HTTP GET request.

    make_request(url, params, headers=None):
        Makes an HTTP GET request to the specified URL with the given parameters and optional headers.

    get_top_videos(query, max_results=3):
        Fetches the top videos related to a given query.

    get_captions(video_id):
        Fetches caption metadata for a given video ID.

    download_and_parse_captions(caption_id):
        Downloads and parses captions in XML format for a given caption ID.

    generate_iframe(video):
        Generates embeddable HTML for a video.
    """

    def __init__(
        self,
        api_key: str,
        sa_credentials_file: str = None,
    ):
        """
        Initializes the RelatedYouTubeVideos class with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key to authenticate requests to the YouTube Data API.
        """
        self.api_key = api_key

        if sa_credentials_file:
            self.credentials = Credentials.from_service_account_file(
                sa_credentials_file,
                scopes=[
                    "https://www.googleapis.com/auth/youtube.force-ssl",
                    "https://www.googleapis.com/auth/youtubepartner",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            )
        self.token = None

    def get_access_token(self):
        """
        Refreshes and retrieves the access token.
        """
        if not self.credentials.valid:
            self.credentials.refresh(Request())
        self.token = self.credentials.token

    def make_request(self, url: str, params: dict, headers: dict = None):
        """
        Makes an HTTP GET request to the specified URL with the given parameters and optional headers.

        Parameters
        ----------
        url : str
            The URL endpoint to which the request is made.
        params : dict
            A dictionary of query parameters to include in the request.
        headers : dict, optional
            A dictionary of HTTP headers to include in the request (default is None).

        Returns
        -------
        dict or None
            The JSON response as a dictionary if the request is successful (status code 200),
            or None if the request fails.
        """
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("An error occurred: %s %s", response.status_code, response.text)
            return None

    def make_oauth_request(self, url, params=None, headers=None):
        """
        Makes an HTTP GET request to the specified URL with the given parameters and optional headers.

        Parameters
        ----------
        url : str
            The URL endpoint to which the request is made.
        params : dict
            A dictionary of query parameters to include in the request.
        headers : dict, optional
            A dictionary of HTTP headers to include in the request (default is None).

        Returns
        -------
        dict or None
            The JSON response as a dictionary if the request is successful (status code 200),
            or None if the request fails.
        """
        if not self.token:
            self.get_access_token()

        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.token}"

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response
        else:
            logger.error("An error occurred: %s %s", response.status_code, response.text)
            return None

    def get_top_videos(self, query: str, max_results: int = 3):
        """
        Fetches the top videos for a given query.

        Parameters
        ----------
        query : str
            The search query to find videos.
        max_results : int, optional
            The maximum number of results to return (default is 3).

        Returns
        -------
        list of dict or None
            A list of dictionaries containing video information, or None if the request fails.
        """
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "order": "relevance",
            "key": self.api_key,
        }

        data = self.make_request(Endpoints.SEARCH, params)
        if data:
            videos = []

            for item in data["items"]:
                video_id = item["id"]["videoId"]
                video_info = {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channelTitle": item["snippet"]["channelTitle"],
                    "publishTime": item["snippet"]["publishTime"],
                    "videoId": video_id,
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                }
                videos.append(video_info)

            return videos
        else:
            return None

    def get_captions(self, video_id: str):
        """
        Fetches caption metadata for a given video ID.

        Parameters
        ----------
        video_id : str
            The ID of the video for which to fetch captions.

        Returns
        -------
        list of dict or None
            A list of dictionaries containing caption metadata, or None if the request fails.
        """
        params = {"part": "snippet", "videoId": video_id, "key": self.api_key}

        data = self.make_request(Endpoints.CAPTIONS, params)
        if data:
            captions = []

            for item in data["items"]:
                if "snippet" in item:
                    captions.append(
                        {
                            "captionId": item["id"],
                            "language": item["snippet"]["language"],
                            "name": item["snippet"]["name"],
                            "trackKind": item["snippet"]["trackKind"],
                            "isAutoSynced": item["snippet"]["isAutoSynced"],
                        }
                    )

            return captions
        else:
            logger.info(f"No captions found for {video_id}")
            return None

    def _download_and_parse_captions(self, caption_id: str):
        """
        Downloads and parses captions in XML format for a given caption ID.

        Parameters
        ----------
        caption_id : str
            The ID of the caption track to download and parse.

        Returns
        -------
        list of dict or None
            A list of dictionaries containing parsed caption data, or None if the request fails.
        """
        logger.warn("Method is not supported")
        url = f"{Endpoints.CAPTIONS}/{caption_id}"
        params = {"tfmt": "xml"}  # Requesting XML format
        headers = {"Accept": "application/xml"}

        response = self.make_oauth_request(url, params=params, headers=headers)

        if response and response.status_code == 200:
            captions_xml = response.content
            # Parse the XML
            root = ET.fromstring(captions_xml)
            captions = []

            for child in root.findall(".//text"):
                start = child.attrib["start"]
                duration = child.attrib.get("dur", "0")
                text = child.text
                captions.append({"start": start, "duration": duration, "text": text})

            return captions
        return None

    def download_and_parse_captions(self, video_id: str):
        """
        Downloads and parses captions in XML format for a given caption ID.

        Parameters
        ----------
        video_id : str
            The ID of the video to download and parse captions.

        Returns
        -------
        list of dict or None
            A list of dictionaries containing parsed caption data, or None if the request fails.
        """
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        captions_text = []

        if captions:
            for cap in captions:
                cap["end"] = round(cap["start"] + cap["duration"], 2)
                captions_text.append(f"{cap['start']} - {cap['end']}: {cap['text']}")

            return captions_text
        return None

    def hhmmss_to_seconds(self, time_str: str) -> int:
        """
        Converts a time string in hh:mm:ss or mm:ss format to seconds.

        Parameters
        ----------
        time_str : str
            The time string in hh:mm:ss or mm:ss format.

        Returns
        -------
        int
            The time in seconds.
        """
        parts = list(map(int, time_str.split(":")))
        if len(parts) == 2:
            m, s = parts
            return m * 60 + s
        elif len(parts) == 3:
            h, m, s = parts
            return h * 3600 + m * 60 + s
        else:
            raise ValueError("Invalid time format, expected hh:mm:ss or mm:ss")

    def generate_iframe(self, video: dict, start: float = None):
        """
        Generates embeddable HTML for a video.

        Parameters
        ----------
        video : dict
            A dictionary containing video information.

        Returns
        -------
        str
            The generated HTML string for embedding the video and displaying captions.
        """
        with open(os.path.join(Path.template_dir, "video_embed.html"), "r") as f:
            template_str = f.read()

        url = f"https://www.youtube.com/embed/{video['videoId']}"

        if start:
            # start = self.hhmmss_to_seconds(start)
            url = f"{url}?start={int(start)}"

        template = Template(template_str)
        html = template.render(url=url, video=video)
        return html

    def find_start_time(self, query: str, captions: str) -> int:
        prompt_template = PromptTemplate(
            input_variables=["question", "captions"],
            template="""Given the following YouTube video captions and the question, determine the start timestamp
            (in seconds) where the answer to the question can be found. Answer should only be in form of a number.

            Question: {question}
            Captions:
            {captions}

            Start Timestamp (in seconds):
            """,
        )
        llm_text = ChatVertexAI(
            model="gemini-pro", credentials=self.credentials, temperature=0.15, max_output_tokens=256
        )
        chain = prompt_template | llm_text

        return chain.invoke({"question": query, "captions": captions}).content


if __name__ == "__main__":
    api_key = APIKeys()

    # Initialize RelatedYouTubeVideos instance with API key
    youtube_api = RelatedYouTubeVideos(
        api_key=api_key.YOUTUBE_API_KEY,
        sa_credentials_file=os.path.join(Path.secrets_dir, api_key.GCLOUD_SERVICE_ACCOUNT_KEY_PATH),
    )

    # Example query to fetch top related videos
    query = """HMMs parameter matrix calculation
    How can one compute the emission and transition matrices for a Hidden Markov Model (HMM) based on a 3-character
    sequence? Additionally, could you provide the relevant formulas for these calculations?"""

    # Get top related videos
    top_videos = youtube_api.get_top_videos(query, max_results=1)

    for idx, video in enumerate(top_videos):
        logger.info(pretty_repr(video))

        # Example usage to get captions for each video
        video_id = video["videoId"]
        captions_info = youtube_api.get_captions(video["videoId"])
        if captions_info:
            captions = youtube_api.download_and_parse_captions(video_id)

            logger.info(pretty_repr(captions))

            start_time = youtube_api.find_start_time(query, captions)
            logger.info(start_time)

        # Generate HTML for embedding the video
        html_output = youtube_api.generate_iframe(video, start=134)
        logger.debug(html_output)

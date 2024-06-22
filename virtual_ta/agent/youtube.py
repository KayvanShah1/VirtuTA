import os
import xml.etree.ElementTree as ET

import requests
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from jinja2 import Template
from rich.pretty import pretty_repr
from settings import APIKeys, Path, get_logger

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

    Methods
    -------
    make_request(url, params, headers=None):
        Makes an HTTP GET request to the specified URL with the given parameters and optional headers.

    get_top_videos(query, max_results=3):
        Fetches the top videos related to a given query.

    get_captions(video_id):
        Fetches caption metadata for a given video ID.

    download_and_parse_captions(caption_id):
        Downloads and parses captions in XML format for a given caption ID.

    generate_html(video, captions):
        Generates embeddable HTML for a video along with its captions.
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
                ],
            )
        self.token = None

    def get_access_token(self):
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

    def download_and_parse_captions(self, caption_id: str):
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
        url = f"{Endpoints.CAPTIONS}/{caption_id}"
        params = {"tfmt": "xml"}  # Requesting XML format
        headers = {"Accept": "application/xml"}

        response = self.make_oauth_request(url, params=params, headers=headers)

        if response:
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

    def generate_iframe(self, video):
        """
        Generates embeddable HTML for a video along with its captions.

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

        template = Template(template_str)
        html = template.render(video=video)
        return html


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
    top_videos = youtube_api.get_top_videos(query, max_results=3)

    for idx, video in enumerate(top_videos):
        logger.info(pretty_repr(video))

        # Example usage to get captions for each video
        captions_info = youtube_api.get_captions(video["videoId"])
        logger.info(pretty_repr(captions_info))
        if captions_info:
            first_caption_id = captions_info[0]["captionId"]
            captions = youtube_api.download_and_parse_captions(first_caption_id)

        # Generate HTML for embedding the video
        html_output = youtube_api.generate_iframe(video)
        logger.debug(html_output)

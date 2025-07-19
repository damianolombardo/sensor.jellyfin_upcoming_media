"""Client."""
import datetime
import requests
import logging

_LOGGER = logging.getLogger(__name__)


class JellyfinClient:
    """Client class"""

    def __init__(self, host, api_key, ssl, port, max_items, user_id, show_episodes):
        """Init."""
        self.data = {}
        self.host = host
        self.ssl = "s" if ssl else ""
        self.port = port
        self.api_key = api_key
        self.user_id = user_id
        self.max_items = max_items
        self.show_episodes = "&GroupItems=False" if show_episodes else ""

    def get_view_categories(self):
        """This will pull the list of all View Categories on Jellyfin"""
        try:
            url = f"http{self.ssl}://{self.host}:{self.port}/UserViews?userId={self.user_id}&api_key={self.api_key}"
            _LOGGER.info("Making API call on URL %s", url)
            api = requests.get(url, timeout=10)
        except OSError:
            _LOGGER.warning("Host %s is not available", self.host)
            self._state = "%s cannot be reached" % self.host
            return

        if api.status_code == 200:
            self.data["ViewCategories"] = api.json()["Items"]

        else:
            _LOGGER.info("Could not reach url %s", url)
            self._state = "%s cannot be reached" % self.host

        return self.data["ViewCategories"]

    def get_data(self, categoryId):
        fields = 'ProviderIds,Overview,RemoteTrailers,CommunityRating,Studios,PremiereDate,Genres,ChildCount,ProductionYear,DateCreated'
        try:
            url = f"http{self.ssl}://{self.host}:{self.port}/Users/{self.user_id}/Items/Latest?Limit={self.max_items}&Fields={fields}&ParentId={categoryId}&api_key={self.api_key}{self.show_episodes}"
            _LOGGER.info("Making API call on URL %s", url)
            api = requests.get(url, timeout=10)
        except OSError:
            _LOGGER.warning("Host %s is not available", self.host)
            self._state = "%s cannot be reached" % self.host
            return

        if api.status_code == 200:
            self._state = "Online"
            self.data[categoryId] = api.json()[: self.max_items]

        else:
            _LOGGER.info("Could not reach url %s", url)
            self._state = "%s cannot be reached" % self.host
            return

        return self.data[categoryId]

    def get_image_url(self, itemId, imageType):
        url = f"http{self.ssl}://{self.host}:{self.port}/Items/{itemId}/Images/{imageType}?maxHeight=360&maxWidth=640&quality=90&userId={self.user_id}&api_key={self.api_key}"
        return url
            
    def get_base_url(self):
        """Return the base URL for the Jellyfin server."""
        protocol = "https" if self.ssl else "http"
        return f"{protocol}://{self.host}:{self.port}"

    def get_image_bytes(self, url):
        """Return the bytes of an image at a URL"""
        response = requests.get(url, timeout=10)
        try:
            response.raise_for_status()
            return response.content
        except Exception as e:
            _LOGGER.error(f"Failed to open image url {url}: {e}")
            return b''

    def get_tvdb_images(tvdbid):
        return  [f"https://artworks.thetvdb.com/banners/movies/{tvdbid}/{t}s/{tvdbid}.jpg" for t in ['poster', 'background']]
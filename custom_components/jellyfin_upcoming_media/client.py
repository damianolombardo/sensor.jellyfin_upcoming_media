"""Client."""
import datetime
import requests
import logging
from io import BytesIO

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
        fields = 'ParentId,ProviderIds,Overview,RemoteTrailers,CommunityRating,Studios,PremiereDate,Genres,ChildCount,ProductionYear,DateCreated'
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
            category_data = api.json()[: self.max_items]

        else:
            _LOGGER.info("Could not reach url %s", url)
            self._state = "%s cannot be reached" % self.host
            return

        # load the images as local assets
        image_types = ['Primary', 'Backdrop', 'Banner', 'Logo', 'Thumb']
        for item in category_data:
            itemId = item.get('Id')
            if itemId:
                for imageType in image_types:
                    image_url = self.get_image_url(itemId, imageType)
                    image_bytes = self.get_image_bytes(image_url)
                    item[f'{imageType}_bytes'] = BytesIO(image_bytes)
            ParentId = item.get('ParentId', None)
            if ParentId:
                for imageType in image_types:
                    image_url = self.get_image_url(ParentId, imageType)
                    image_bytes = self.get_image_bytes(image_url)
                    item[f'{imageType}_parent_bytes'] = BytesIO(image_bytes)

        self.data[categoryId] = category_data

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
        if response.status_code == 200:
            return response.content
        elif response.status_code == 404:
            _LOGGER.warning("Image not found at URL: %s", url)
        elif response.status_code == 403:
            _LOGGER.warning("Access forbidden to image at URL: %s", url)
        else:
            _LOGGER.error("Error fetching image at URL %s: %s", url, response.status_code)
        return b''

    def get_tvdb_images(self, tvdbid, img_type: str, media_type: str):
        return  f"https://artworks.thetvdb.com/banners/{media_type}/{tvdbid}/{img_type}s/{tvdbid}.jpg"
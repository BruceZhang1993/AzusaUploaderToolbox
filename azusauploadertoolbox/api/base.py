import socket
from abc import ABCMeta, abstractmethod, abstractproperty
from contextlib import closing
from enum import Enum
from typing import Tuple, List, Dict, Any


class PrivacyStatus(str, Enum):
    private = 'Private'
    public = 'Public'
    unlisted = 'Unlisted'


class VideoProperty(str, Enum):
    filepath = 'File Path'
    title = 'Title'
    description = 'Description'
    tags = 'Tags'
    category = 'Category ID'
    privacy = 'Privacy Status'


class BaseApi(metaclass=ABCMeta):
    def __init__(self, progress_cb):
        self._cb = progress_cb

    def update_progress(self, properties, progress: float):
        self._cb(properties, progress)

    @staticmethod
    def find_free_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('127.0.0.1', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    @property
    @abstractmethod
    def supported_video_properties(self) -> List[Tuple[VideoProperty, Any]]:
        """
        Returns supported properties and its default value if available

        :return:
        """
        pass

    @property
    @abstractmethod
    def has_credentials(self) -> bool:
        """
        This property saves the auth state of this api

        :rtype: bool
        :return: True if this api has been authed
        """
        pass

    @abstractmethod
    def load_credentials(self) -> None:
        """
        This method loads the existed credentials if `has_credentials` returns true.
        Else this method starts a process to get credentials from login api.

        :rtype: None
        :return: nothing
        """
        pass

    @abstractmethod
    def run(self, properties: Dict[VideoProperty, Any]) -> Tuple[bool, str]:
        """
        This method process the upload and returns the status and error message if failed.

        :rtype: Tuple[bool, str]
        :return: status, error message
        """
        pass

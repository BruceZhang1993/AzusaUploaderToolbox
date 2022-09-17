import socket
from abc import ABCMeta, abstractmethod, abstractproperty
from contextlib import closing
from typing import Tuple


class BaseApi(metaclass=ABCMeta):
    @staticmethod
    def find_free_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('127.0.0.1', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

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
    def run(self) -> Tuple[bool, str]:
        """
        This method process the upload and returns the status and error message if failed.

        :rtype: Tuple[bool, str]
        :return: status, error message
        """
        pass

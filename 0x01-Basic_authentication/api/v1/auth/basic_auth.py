#!/usr/bin/env python3
""" Definition of class BasicAuth
"""
import base64
from .auth import Auth
from typing import TypeVar, Union

from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class This class inherits from
    Auth and serves as a basic authentication
    """
    def extract_base64_authorization_header(
      self,
      authorization_header: str
    ) -> str:
        """
        Method to extract the Base64 value from the Authorization header

        :param authorization_header: _description_
        :type authorization_header: str
        :return: _description_
        :rtype: str
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        token = authorization_header.split(" ")[-1]
        return token

    def decode_base64_authorization_header(
      self, base64_authorization_header: str
    ) -> str:
        """
        Method to decode a Base64 string

        :param base64_authorization_header: _description_
        :type base64_authorization_header: str
        :return: _description_
        :rtype: str
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(decoded)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
      self,
      decoded_base64_authorization_header: str
    ) -> Union[str, str]:
        """
        Method to extract the email and password from a Base64 string

        :param decoded_base64_authorization_header: _description_
        :type decoded_base64_authorization_header: str
        :return: _description_
        :rtype: Union[str, str]
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(
      self, user_email: str,
      user_pwd: str
    ) -> TypeVar['User']:
        """
        Method to retrieve a User instance based on email and password

        :return: _description_
        :rtype: _type_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar['User']:
        """
        Method to retrieve the current User instance

        :return: _description_
        :rtype: _type_
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)

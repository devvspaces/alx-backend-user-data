#!/usr/bin/env python3
"""
Hashed password module
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User


U = TypeVar('U', bound=User)


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string and returns it in bytes form

    :param password: password to hash
    :type password: str
    :return: hashed password
    :rtype: bytes
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a uuid and
    return its string representation
    :return: uuid string
    """
    return str(uuid4())


class Auth:
    """Defines a class Auth for user authentication
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object
        
        :param email: user's email address
        :type email: str
        :param password: user's password
        :type password: str
        :return: newly created user object
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials
        :param email: user's email address
        :type email: str
        :param password: user's password
        :type password: str
        :return: True if the user's credentials are valid, else False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session_id for an existing user and update the user's
        session_id attribute
        :param email: user's email address
        :type email: str
        :return: newly created session_id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Takes a session_id and returns the corresponding user

        :param session_id: user's session_id
        :type session_id: str
        :return: user object or None
        """

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Take a user_id and destroy that user's session and update their
        session_id attribute to None
        
        :param user_id: user's id
        :type user_id: int
        :return: None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token uuid for a user identified by the given email
        
        :param email: user's email address
        :type email: str
        :return: reset_token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password

        :param reset_token: user's reset_token
        :type reset_token: str
        :param password: user's new password
        :type password: str
        :return: None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)

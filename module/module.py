# coding: utf-8
"""Shinken WebUI LDAPv3 authentication module"""
from __future__ import unicode_literals

from ldap3 import SUBTREE, Connection, Server
from ldap3.core.exceptions import (LDAPBindError, LDAPException,
                                   LDAPPasswordIsMandatoryError,
                                   LDAPSocketOpenError)
from shinken.basemodule import BaseModule
from shinken.log import logger


# pylint: disable=invalid-name
properties = {
    'daemons': ['broker', 'webui'],
    'type': 'authentication',
    'external': False
}


def get_instance(plugin):
    """Returns a new instance to the module manager"""
    logger.debug(
        "[auth-ldap3] Get an LDAPv3 UI module for plugin %s",
        plugin.get_name()
    )
    return LDAPv3Module(plugin)


class LDAPv3Module(BaseModule):
    """LDAPv3 authentication module"""

    # pylint: disable=abstract-method,too-many-instance-attributes

    def __init__(self, modconf):
        super(LDAPv3Module, self).__init__(modconf)
        self.app = None

        try:
            self.ldap_uri = getattr(modconf, 'ldap_uri')
            self.base_dn = getattr(modconf, 'base_dn')
            self.search_filter = getattr(modconf, 'search_filter')
        except AttributeError:
            logger.error("[auth-ldap3] Missing LDAP server URI")
            raise

        self.bind_dn = getattr(modconf, 'bind_dn', None)
        self.bind_password = getattr(modconf, 'bind_password', None)

        self.connection = None
        self.server = Server(self.ldap_uri)

    def load(self, app):
        """Load the WebUI application"""
        self.app = app

    def bind(self, username, password):
        """Connect and bind to the LDAP server"""
        logger.info("[auth-ldap3] Connecting to the LDAP server...")
        try:
            self.connection = Connection(
                self.server,
                user=username,
                password=password,
                auto_bind=True
            )
        except LDAPSocketOpenError as err:
            logger.error(
                "[auth-ldap3] Failed to connect to the LDAP server: %s", err
            )
            raise
        except (LDAPBindError, LDAPPasswordIsMandatoryError) as err:
            logger.error(
                "[auth-ldap3] Failed to bind to the LDAP server: %s", err
            )
            raise

    def unbind(self):
        """Reset the connection"""
        self.connection.unbind()

    def check_auth(self, username, password):
        """Authenticate a user"""
        if not self.app.datamgr.get_contact(username):
            logger.info("[auth-ldap3] User not found in contacts: %s", username)
            return False

        try:
            self.bind(self.bind_dn, self.bind_password)
        except LDAPException:
            return False

        self.connection.search(
            search_base=self.base_dn,
            search_filter=self.search_filter % (username, username),
            search_scope=SUBTREE,
            attributes=['mail', 'uid']
        )

        # Look for the user in the LDAP directory
        for entry in self.connection.entries:
            if entry.uid == username or entry.email == username:
                user_dn = entry.entry_dn
                self.unbind()
                break
        else:
            logger.info("[auth-ldap3] No matching user: %s", username)
            self.unbind()
            return False

        # Bind with the user's credentials
        try:
            self.bind(user_dn, password)
        except LDAPException:
            return False

        logger.info(
            "[auth-ldap3] User successfully authenticated: %s", username
        )
        self.unbind()
        return True

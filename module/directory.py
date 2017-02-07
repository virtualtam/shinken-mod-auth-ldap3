# coding: utf-8
"""LDAP connection wrappers"""
from __future__ import unicode_literals

from ldap3 import SUBTREE, Connection, Server
from ldap3.core.exceptions import (LDAPBindError, LDAPException,
                                   LDAPPasswordIsMandatoryError,
                                   LDAPSocketOpenError)
from shinken.log import logger


class LDAPConnection(object):
    """Generic LDAP connection wrapper"""

    def __init__(self, modconf):
        try:
            self.server = Server(getattr(modconf, 'ldap_uri'))
            self.base_dn = getattr(modconf, 'base_dn')
            self.search_filter = getattr(modconf, 'search_filter')
        except AttributeError:
            logger.error("[WebUI-auth-ldap3] Missing LDAP server information")
            raise

        self.bind_dn = getattr(modconf, 'bind_dn', None)
        self.bind_password = getattr(modconf, 'bind_password', None)
        self.connection = None
        self.user_attributes = []

    def bind(self, username, password):
        """Connect and bind to the LDAP server"""
        logger.info("[WebUI-auth-ldap3] Connecting to the LDAP server...")
        try:
            self.connection = Connection(
                self.server,
                user=username,
                password=password,
                auto_bind=True
            )
        except LDAPSocketOpenError as err:
            logger.error(
                "[WebUI-auth-ldap3] Failed to connect to the LDAP server: %s",
                err
            )
            raise
        except (LDAPBindError, LDAPPasswordIsMandatoryError) as err:
            logger.error(
                "[WebUI-auth-ldap3] Failed to bind to the LDAP server: %s",
                err
            )
            raise

    def unbind(self):
        """Reset the connection"""
        self.connection.unbind()

    def get_user_dn(self, username):
        """Retrieve a user's DN"""
        raise NotImplementedError

    def check_auth(self, username, password):
        """User lookup and authentication"""
        try:
            self.bind(self.bind_dn, self.bind_password)
        except LDAPException:
            return False

        # Look for the user in the LDAP directory
        self.connection.search(
            search_base=self.base_dn,
            search_filter=self.search_filter % (username, username),
            search_scope=SUBTREE,
            attributes=self.user_attributes
        )

        user_dn = self.get_user_dn(username)
        self.unbind()
        if not user_dn:
            logger.info("[WebUI-auth-ldap3] No matching user: %s", username)
            return False

        # Bind with the user's credentials
        try:
            self.bind(user_dn, password)
        except LDAPException:
            return False

        logger.info(
            "[WebUI-auth-ldap3] User successfully authenticated: %s", username
        )
        self.unbind()
        return True


class OpenLDAPConnection(LDAPConnection):
    """OpenLDAP connection wrapper"""

    def __init__(self, modconf):
        super(OpenLDAPConnection, self).__init__(modconf)
        self.user_attributes = ['mail', 'uid']

    def get_user_dn(self, username):
        for entry in self.connection.entries:
            if entry.uid == username or entry.mail == username:
                user_dn = entry.entry_dn
                return user_dn
        return None


class ActiveDirectoryConnection(LDAPConnection):
    """ActiveDirectory (AD) connection wrapper"""

    def __init__(self, modconf):
        super(ActiveDirectoryConnection, self).__init__(modconf)
        self.user_attributes = ['mail', 'samaccountname']

    def get_user_dn(self, username):
        for entry in self.connection.entries:
            if entry.samaccountname == username or entry.mail == username:
                user_dn = entry.entry_dn
                return user_dn
        return None

# coding: utf-8
"""Shinken WebUI LDAPv3 authentication module"""
from __future__ import absolute_import, unicode_literals

from shinken.basemodule import BaseModule
from shinken.log import logger

from .directory import ActiveDirectoryConnection, OpenLDAPConnection


# pylint: disable=invalid-name
properties = {
    'daemons': ['broker', 'webui'],
    'type': 'authentication',
    'external': False
}


def get_instance(plugin):
    """Returns a new instance to the module manager"""
    logger.debug(
        "[WebUI-auth-ldap3] Get an LDAPv3 UI module for plugin %s",
        plugin.get_name()
    )
    return LDAPv3Module(plugin)


class LDAPv3Module(BaseModule):
    """LDAPv3 authentication module"""

    # pylint: disable=abstract-method

    def __init__(self, modconf):
        super(LDAPv3Module, self).__init__(modconf)
        self.app = None

        mode = getattr(modconf, 'mode', 'openldap')

        if mode == 'ad':
            self.directory = ActiveDirectoryConnection(modconf)
        elif mode == 'openldap':
            self.directory = OpenLDAPConnection(modconf)
        else:
            raise Exception("Unsupported LDAP mode")

    def load(self, app):
        """Load the WebUI application"""
        self.app = app

    def check_auth(self, username, password):
        """Check a user can authenticate"""
        if not self.app.datamgr.get_contact(username):
            logger.info(
                "[WebUI-auth-ldap3] User not found in contacts: %s", username
            )
            return False

        return self.directory.check_auth(username, password)

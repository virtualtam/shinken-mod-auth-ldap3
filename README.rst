shinken-mod-auth-ldap3
======================

.. image:: https://img.shields.io/travis/virtualtam/shinken-mod-auth-ldap3/master.svg?style=flat-square&label=master
   :target: https://travis-ci.org/virtualtam/shinken-mod-auth-ldap3
   :alt: Travis build status

.. image:: https://img.shields.io/github/license/virtualtam/shinken-mod-auth-ldap3.svg?style=flat-square
   :target: http://www.gnu.org/licenses/agpl-3.0.html
   :alt: GNU Affero General Public License v3.0

`LDAP <https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol>`_
authentication module for
`Shinken <https://github.com/naparuba/shinken>`_
`WebUI 2 <https://github.com/shinken-monitoring/mod-webui>`_,
relying on the native Python `ldap3 <https://github.com/cannatag/ldap3>`_ package.

Supported LDAP implementations:

* `ActiveDirectory <https://msdn.microsoft.com/en-us/library/aa362244(v=vs.85).aspx>`_
* `OpenLDAP <http://www.openldap.org/>`_
* `389 Directory Server <http://www.port389.org/>`_ (use the ``openldap`` mode)

Setup
-----

This module can be installed from `shinken.io <http://shinken.io/>`_::

  shinken@myhost $ shinken install auth-ldap3

A commented configuration file is copied to ``/etc/shinken/modules/auth_ldap3.cfg``,
that must be edited according to your LDAP directory settings.

To enable this authentication module, add it to ``/etc/shinken/modules/webui2.cfg``::

  define module {
      module_name     webui2
      ...

      modules   ..., auth-ldap3, ...

  }

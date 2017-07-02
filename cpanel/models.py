# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import ldap
#from ldapdb.models.fields import (CharField, ImageField, ListField, IntegerField)
#import ldapdb.models

# Create your models here.
'''
class LdapAdminUser(object):
    """ 
    Class for representing an LDAP user entry.
    """
    managed=False
    # LDAP meta-data
    base_dn = b"dc=example,dc=tld"
    object_classes = ['organizationalRole', 'simpleSecurityObject', 'extensibleObject']
    # inetOrgPerson
    dn=CharField(db_column='dn', max_length=200)
    username= CharField(db_column='cn', max_length=200, primary_key=True) 
    description = CharField(db_column='description', max_length=200)
    email = CharField(db_column='email',max_length=200)
    status = CharField(db_column='status')
    password = CharField(db_column='userPassword')
    is_active=True
    is_staff=True
    is_superuser=True
    last_login = models.DateTimeField() 
    def __unicode__(self):
        return self
'''

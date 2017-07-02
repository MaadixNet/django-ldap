from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User, Permission
from django.conf import settings
import ldap
import re

import logging
#from .models import LdapAdminUser 

log = logging.getLogger(__name__)
INTERNAL_USER = None


class LDAPUserAuthBackend(RemoteUserBackend):

    create_unknown_user = False

    def authenticate(self, username=None, password=None, **kwargs):
        # if username or password is not given, then skip
        if not username or not password:
            return None

        try:
            # initialize connection to ActiveDirectory  the property contains ldap url like ldap://hostname:389
            connect = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)

            # if user just provide account name portion 'fistName.lastName' on username
            # then use your company default domain
            if '@' not in username:
                bind_connection=connect.simple_bind_s('cn=' + username + ',' + settings.AUTH_LDAP_BASE_DN, password)
                base_dn = 'dc=example,dc=tld'
                search_filter = '(&(objectClass=extensibleObject)(cn=' + username + '))'
            else:
                # if user provides domain info in username like 'myCompanyDomain\firstName.lastName'
                domain,  account_name = username.split('@')
                connect.simple_bind_s('{user_name}@{domain_name}'.format(user_name=account_name, domain_name=domain), password)
                base_dn = 'cn=users,dc={domain_name},dc=com,'.format(domain_name=domain)
                search_filter = '(&(objectClass=user)(sAMAccountName=' + account_name + '))'
                username = account_name
            result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter )
            log.debug(result)

            # if search result is found, result will be [(user_dn,{'memberOf':['group cn'...]}]
            if result:
                result_user_dn, result_dict = result[0]

                if result_user_dn:
                        user, created = User.objects.get_or_create(username=username)
                        
                        first_name = username
                        last_name = username
                        user.username=username
                        user.first_name = first_name
                        user.last_name = last_name
                        user.is_active = True
                        user.is_staff = True
                        user.is_superuser = True
                        user.results= result[0]
                        user.cn=result[0][0]
                        user.data=result[0][1]
                        user.bind = bind_connection
                        #user=LdapAdminUser()
                        global INTERNAL_USER
                        INTERNAL_USER = user
                        return user
            log.info('fail to authorize user, username: {}'.format(username))
            return None
        except ldap.LDAPError as e:
            log.warning('authentication error, detail: {}'.format(str(e)))
            return None
        #finally:
            #connect.unbind_s()

    def get_user(self, user_id):
        # don't want to go back to database.
        # once auth via LDAP successful, that is the user
        # because of the user_id is for user passed auth via this backend
        global INTERNAL_USER
        return INTERNAL_USER

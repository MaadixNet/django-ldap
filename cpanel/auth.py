from django.contrib.auth.models import User
from .models import LdapAdminUser
import ldap
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
#


class Backend(ModelBackend):
    def authenticate(self, username=None, password=None):
        pass
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_user_by_username(self,username):
        try:
            return User.objects.get(username=username)
        except:
            return None
#


class LdapBackend(Backend):
    def _get_ldap_user_by_username(self, conn, username, dn):
        try:
            #search_scope = ldap.SCOPE_SUBTREE
            search_scope = "dc=example,dc=tld"
            retrieve_attributes = None
            search_filter = "cn="+username
            result_id = conn.search(dn,search_scope,search_filter,retrieve_attributes)
            result_set = []
            ldap_user = {}
            while 1:
                result_type, result_data = conn.result(result_id,0)
                if (result_data ==[]):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            ldap_user = result_set[0][0][1]
            return ldap_user
        except:
            return {}


class CustomLdapBackend(LdapBackend):
    def authenticate(self, username=None, password=None):
        try:
            credentials = [username, password]
            if (None in credentials) or ('' in credentials):
                return None

            ldap.set_option( ldap.OPT_REFERRALS,0 )
            try:
                conn = ldap.initialize('ldap://localhost/')
                conn.simple_bind_s( 'cn=' + username + ',dc=example,dc=tld', password )
            except:
                conn.unbind_s()
                return None

            user = self.get_user_by_username( username=username )

            if user is None:
                user = User(username=username, password='')
                user.save()
                user = self.get_user_by_username(username)
                ldap_user = self._get_ldap_user_by_username(conn=conn, 
                        username=username,dn='dc=example,dc=tld' 
                    )

                if ldap_user is not None:
                    try:
                        user.first_name = ldap_user['cn'][0]
                    except:
                        pass
                    try:
                        user.last_name = ldap_user['cn'][0]
                    except:
                        pass
                    try:
                        user.email = ldap_user['mail'][0]
                    except:
                        pass
                user.save()
                user = self.get_user_by_username(username=username)
                user_profile = UserProfile(user=user)
                user_profile.save()
                user = self.get_user_by_username(username=username)
            conn.unbind_s()


            user.set_password(password)
            user.save()
            return user
        except:
            return None
#


class SettingsBackend(Backend):
    def authenticate(self, username=None, password=None ):

        try:
           # if username not in settings.ADMIN_CREDENTIALS :
           #     return None

            user = self.get_user_by_username(username = username)
            if user is None:
                # create one
                user = User(username=username, password=password )
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        except:
            return None
#

import ldap


LDAP = ldap.initialize("ldap://ldap.iiit.ac.in")

uid = 2019112012
result = LDAP.search_s(
    "ou=users,dc=iiit,dc=ac,dc=in", ldap.SCOPE_SUBTREE, filterstr=f"(uid={uid})"
)

print(result)

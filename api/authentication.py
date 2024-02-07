from rest_framework.authentication import TokenAuthentication as BaseTokenAuth

# If we want to use bearer tokens, add a lil' override 
class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'
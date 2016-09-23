import jwt

class RosefireError(Exception):
    pass

class AuthData():

    def __init__(self, username, name, provider, group, issued_at):
        self.username = username
        self.provider = provider
        self.group = group
        self.name = name
        self.issued_at = issued_at
        self.email = username + "@rose-hulman.edu"

class RosefireTokenVerifier():

    def __init__(self, secret):
        self.secret = secret

    def verify(self, token):
        decodedToken = jwt.decode(token, self.secret)
        iat = decodedToken.get("iat")
        uid = decodedToken["d"].get("uid")
        group = decodedToken["d"].get("group")
        name = decodedToken["d"].get("name")
        provider = decodedToken["d"].get("provider")
        return AuthData(uid, name, provider, group, iat)



if __name__ == "__main__":
   registry_token = "59c300ed7fa9d438198293e9cb675290fcf40988c93103b10b997dc0329c6aa58d7d0f1c244ffd41a0a24e8e04d089238oVFqR4JfVWV/+sohxs6u2He6uOd6ZpFovwiRNam8OUb6kyk6BLktxRGT4/sq6jtYHS7Q/cDH4MmUml8n89i9HL/AIQhzU3HjuIKJS96JBA="
   token = get_token(registry_token, "rockwotj@rose-hulman.edu", "Pa$sW0rd")
   secret = "secret"
   user_info = RosefireTokenVerifier(secret).verify(token)
   print user_info.email
   print user_info.issued_at

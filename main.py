import logging
import os
import json

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import utils

from rosefire import RosefireTokenVerifier
from models import Password
from handlers.base_handlers import BasePage, BaseAction, BaseHandler
 

# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    # Example of a Jinja filter (useful for formatting data sometimes)
    #   jenv.filters["time_and_date_format"] = date_utils.time_and_date_format
    return jenv

jinja_env = __init_jinja_env()


ROSEFIRE_SECRET = "wUHg1XTo3CsiPdvIyvCD"

class PasswordsPage(BasePage):
    def update_values(self, email, values):
        values["password_query"] = utils.get_query_for_all_OBJECTS_for_email(email)
        
    def get_template(self):
        return "templates/password-list.html"

class LoginPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user or "user_info" in self.session:
            self.redirect("/passwords")
            return
        template = jinja_env.get_template("templates/login.html")
        values = {"login_url": users.create_login_url("/passwords")}
        self.response.out.write(template.render(values))

class LoginHandler(BaseHandler):
    def get(self):
        if "user_info" not in self.session:
            token = self.request.get('token')
            auth_data = RosefireTokenVerifier(ROSEFIRE_SECRET).verify(token)
            user_info = {"name": auth_data.name,
                         "username": auth_data.username,
                         "email": auth_data.email,
                         "role": auth_data.group}
            self.session["user_info"] = json.dumps(user_info)
        self.redirect(uri="/passwords")

class LogoutHandler(BaseHandler):
    def get(self):
        del self.session["user_info"]
        self.redirect(uri="/")
    
class InsertPasswordAction(BaseAction):
    def handle_post(self, email):
        if self.request.get("password_entity_key"):
            password_key = ndb.Key(urlsafe=self.request.get("password_entity_key"))
            password = password_key.get()
        else:
            password = Password(parent=utils.get_parent_key_for_email(email))
    
        password.service = self.request.get("service")
        password.username = self.request.get("username")
        password.password = self.request.get("password")
        password.put()
        self.redirect(self.request.referer)


class DeletePasswordAction(BaseAction):
    def handle_post(self, email):
        password_key = ndb.Key(urlsafe=self.request.get("password_to_delete_key"))
        password_key.delete()
        self.redirect(self.request.referer)


config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'wUHg1XTo3CsiPdvIyvCD',
}

app = webapp2.WSGIApplication([
    ("/", LoginPage),
    ("/login", LoginHandler),
    ("/logout", LogoutHandler),
    ("/passwords", PasswordsPage),
    ("/action/insert-password", InsertPasswordAction),
    ("/action/delete-password", DeletePasswordAction)
], config=config, debug=True)


import logging
import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import utils

from models import Password
from handlers.base_handlers import BasePage, BaseAction


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




class PasswordsPage(BasePage):
    def update_values(self, email, values):
        values["password_query"] = utils.get_query_for_all_OBJECTS_for_email(email)
        
    def get_template(self):
        return "templates/password-list.html"

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/passwords")
            return
        template = jinja_env.get_template("templates/login.html")
        values = {"login_url": users.create_login_url("/passwords")}
        self.response.out.write(template.render(values))
        
    
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


app = webapp2.WSGIApplication([
    ("/", LoginPage),
    ("/passwords", PasswordsPage),
    ("/action/insert-password", InsertPasswordAction),
    ("/action/delete-password", DeletePasswordAction)
], debug=True)


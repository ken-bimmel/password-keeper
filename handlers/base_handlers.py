
from google.appengine.api import users
import webapp2

import main

from email import email

# Potentially helpful (or not) superclass for *logged in* pages and actions (assumes app.yaml gaurds for login)

### Pages ###
class BasePage(webapp2.RequestHandler):
    """Page handlers should inherit from this one."""
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")
            return
        email = user.email().lower()
        values = {"user_email": email,
                  "logout_url": users.create_logout_url("/")}
        
        self.update_values(email, values)  
        template = main.jinja_env.get_template(self.get_template())
        self.response.out.write(template.render(values))


    def update_values(self, email, values):
        # Subclasses should override this method to add additional data for the Jinja template.
        pass


    def get_template(self):
        # Subclasses must override this method to set the Jinja template.
        raise Exception("Subclass must implement handle_post!")



### Actions ###

class BaseAction(webapp2.RequestHandler):
    """ALL action handlers should inherit from this one."""
    def post(self):
        user = users.get_current_user()
        if not user:
            raise Exception("Missing user!")
        email = user.email().lower()
        self.handle_post(email)  # TODO: Update what is passed to subclass function as needed


    def get(self):
        self.post()  # Action handlers should not use get requests.


    def handle_post(self, email):
        # Subclasses must override this method to handle the request.
        raise Exception("Subclass must implement handle_post!")

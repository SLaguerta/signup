#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

form="""
<form method= "post">

    <h2>User Signup</h2>
    <label> Username
    <input type="text" name="username" value="">
    <span style="color:red">%(error_username)s</span>
    </label>
    <br>
    <label> Password
    <input type="password" name="password" value="">
    <span style = "color:red">%(error_password)s</span>
    </label>
    <br>
    <label>Verify Password
    <input type="password" name="verify" value="">
    <span style="color:red">%(error_verify)s</span>
    </label>
    <br>

    <label>Email (optional)
    <input type="text" name ="email" value="%(email)s">
    <span style="color:red">%(error_email)s</span>
    </label>
    <div style="color:red">%(error)s</div>
    <input type ="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
     return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", username="", email="", error_username="",
                    error_password="", error_verify="", error_email=""):
        self.response.out.write(form % {"error":error, "username":username,
                                        "email":email, "error_username":error_username, "error_password":error_password,
                                        "error_verify":error_verify, "error_email":error_email
                                        })

    def get(self):
        self.write_form()

    def post(self):
        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username = cgi.escape(username, True)
        password = cgi.escape(password, True)
        verify = cgi.escape(verify, True)
        email = cgi.escape(email, True)

        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        if not valid_username(username):
            error_username = "That's not a valid username."
            error = True
        if not valid_password(password):
            error_password = "That's not a valid password. Try again."
            error = True
        elif password != verify:
            error_verify = "Passwords do not match. Please re-enter."
            error = True
        if not valid_email(email):
            error_email = "That's not a valid email."
            error = True

        if error:
            self.write_form("That doesn't look right", username, email, error_username, error_password, error_verify, error_email)

        else:
             self.redirect("/welcome?username="+username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, " + username + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)

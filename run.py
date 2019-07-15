#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import os
import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route("/")  # route
def index():  # view
    return render_template("index.html")


@app.route("/about")
def about():
    data = []
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    # So in my template, I'm going to refer to this data that we've passed through as company.
    return render_template("about.html", page_title="About", company=data)


# whenever we look at our about url with something after it, it will be passed into this view:
@app.route("/about/<member_name>")
def about_member(member_name):  # a new view
    member = {}  # an empty object
    with open("data/company.json", "r") as json_data:  # read in our json
        data = json.load(json_data)  # store in variable 'data' as json
        for obj in data:  # iterate through data
            if obj["url"] == member_name:  # if the url for this element is equal to member name
                # then our member object should be equal to our current object (in about.html)
                member = obj

    # so with that in place, the member name will link us to whatever member object we specify:
    # e.g. to test if working:
    # return "<h1>" + member["name"] + "</h1>"
    # OR
    # return "<h1>" + member["description"] + "</h1>"
    # But what we will do is create a member.html page to link to:
    return render_template("member.html", member=member)


"""
by default, all of Flask's views will handle a GET request, 
but when we need to start handling anything outside of that, 
such as a POST, or the other methods DELETE or PUT, 
then we need to explicitly state that our route can accept that.
"""


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we got your message".format(request.form["name"]))

    return render_template("contact.html", page_title="Contact")


@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

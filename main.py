# cafe website connected to the cafe api
import requests
from flask import Flask, render_template, request, redirect, url_for
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField
import os


class NewCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("google map url", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Address", validators=[DataRequired()])
    seats = BooleanField("Seating?")
    has_toilet = BooleanField("Bathroom available?")
    has_wifi = BooleanField("Wifi available?")
    has_sockets = BooleanField("Plug ins available?")
    can_take_calls = BooleanField("Can they take calls?")
    coffee_price = StringField("What does the coffee Cost?")
    submit = SubmitField("Submit Post")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MY_SECRET_KEY')
Bootstrap(app)

my_api_key = os.environ.get('MY_API_KEY')
api_requests = os.environ.get('api_requests')


header = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip, deflate, br",
    }


@app.route('/', methods=['POST', 'GET'])
def home():
    form = NewCafeForm()
    cafes = requests.get(f"{api_requests}/all")
    print(cafes)
    json_cafe = cafes.json()
    if form.validate_on_submit():
        # create new record
        new_cafe = {
            'name': request.form.get('name'),
            'map_url': request.form.get('map_url'),
            'img_url': request.form.get('img_url'),
            'location': request.form.get('location'),
            'seats': request.form.get('seats'),
            'has_toilet': request.form.get('has_toilet'),
            'has_wifi': request.form.get('has_wifi'),
            'has_sockets': request.form.get('has_socket'),
            'can_take_calls': request.form.get('can_take_calls'),
            'coffee_price': request.form.get('coffee_price'),
            'key': "3S689lF9aQCIxO",
        }
        print(new_cafe)
        new_post = requests.post(f"{api_requests}/add", json=new_cafe, headers=header)
        print(new_post.text)
        return redirect(url_for('home'))

    return render_template('index.html', all_cafes=json_cafe, form=form)


if __name__ == '__main__':
    app.run(debug=True)

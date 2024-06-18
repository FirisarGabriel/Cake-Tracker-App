from flask import Flask, render_template, request, url_for, redirect 
from pymongo import MongoClient 
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_database 
members = db.members 

def next_birthday(birthdate):
    today = datetime.today()
    try:
        birthdate = datetime.strptime(birthdate, '%d.%m.%Y') 
    except (ValueError, TypeError):
        return today 
    birthdate_this_year = birthdate.replace(year=today.year)

    if birthdate_this_year < today:
        birthdate_this_year = birthdate_this_year.replace(year=today.year + 1)

    return birthdate_this_year

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d.%m.%Y')
    except ValueError:
        return 'Invalid date'


@app.route("/", methods=('GET', 'POST'))
def index():
    all_members = list(members.find())
    for member in all_members:
        member['birthdate'] = format_date(member['birthdate'])

    all_members.sort(key=lambda x: next_birthday(x['birthdate']))

    if all_members:
        next_birthdate = min(next_birthday(member['birthdate']) for member in all_members)
        days_until_next_birthday = (next_birthdate - datetime.today()).days
    else:
        days_until_next_birthday = None

    return render_template('index.html', members = all_members, days_until_next_birthday = days_until_next_birthday)

@app.route("/add_member", methods=['GET', 'POST'])
def add_member():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        country = request.form['country']
        city = request.form['city']

        try:
            birthdate_obj = datetime.strptime(birthdate, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
            if age < 18:
                return render_template('add_member.html', error="Member must be at least 18 years old.")
        except ValueError:
            return render_template('add_member.html', error="Invalid birthdate format.")
        
        existing_member = members.find_one({
            'firstname': firstname,
            'lastname': lastname,
            'country': country,
            'city': city
        })
        if existing_member:
            return render_template('add_member.html', error="A member with the same name and location already exists.")

        members.insert_one({
            'firstname': firstname, 
            'lastname': lastname,
            'birthdate': birthdate,
            'country': country,
            'city': city,
        })
        return redirect(url_for('index'))
    return render_template('add_member.html')

@app.post("/<id>/delete/")
def delete(id): 
    members.delete_one({"_id":ObjectId(id)}) 
    return redirect(url_for('index')) 


if __name__ == "__main__":
    app.run(debug=True) 
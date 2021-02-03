# Exercise 18.1: Update the Guess a secret number game
# Now that you've learned how to save an object into a database and read from it, you can update the "Guess a secret number" game.


import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("index.html", user=user)



@app.route("/addnew", methods=["POST"])
def addnew():
    name = request.form.get("name")
    email = request.form.get("email")

    # Kreiram nasumični broj"
    secret_number = random.randint(1, 30)

    # Provjeravam postoji li već User u databazi
    user = db.query(User).filter_by(email=email).first()

    # Ako ne postoji User, stvaram ga i pospremam objekt u bazu
    if not user:
        user = User(name=name, email=email, secret_number=secret_number)

        db.add(user)
        db.commit()

    # Spremam User email u cookie
    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    # Vadim Usera iz databaze po mailu
    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message = "Correct! The secret number is {0}".format(str(guess))

        # Stvaram novi broj
        new_secret = random.randint(1, 30)

        # Updejtam Userov broj
        user.secret_number = new_secret

        # Updejtam objekt u databazi
        db.add(User)
        db.commit()

    elif guess > user.secret_number:
        message = "Your guess is not correct... try something smaller."

    elif guess < user.secret_number:
        message = "Your guess is not correct... try something bigger."

    return render_template("result.html", message=message)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
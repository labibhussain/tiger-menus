from app import app, cas
from flask_cas import login_required
from app.forms import AddFoodForm
from flask import render_template, flash, redirect, url_for, request
from app.models import getUser
from app import views

@app.route('/finder', methods=['GET', 'POST'])
@login_required
def finder():
    user = getUser(cas.username)

    form = AddFoodForm()

    if form.validate_on_submit():
        food = form.food.data.lower()
        form.food.data = None
        if food not in user.prefs:
            if len(food) > 40:
                flash("pls don't spam", "error")
            else:
                user.prefs.append(food)
                user.save()
        return redirect(url_for('finder'))
        #flash("New entry added!", "success")

    # some magic to match preferences to this weeks meals
    # then pass it to render_template
    matches = "placeholders for when foods are being served"

    return render_template('finder.html', 
    prefs=user.prefs, form=form,
    meal='dinner',
    title=views.title, message=views.message,
    i=0, nextWeek=views.nextWeek, matches=matches)


@app.route('/r', methods=['POST'])
@login_required
def r():
    user = getUser(cas.username)

    food = request.form['food']
    if food in user.prefs:
        user.prefs.remove(food)
        user.save()

    return redirect(url_for('finder'))
    
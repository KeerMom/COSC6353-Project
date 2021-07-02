from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return redirect(url_for('views.fuel_quote_form'))
    else:
        return redirect(url_for('views.fuel_quote_form'))
        # return redirect(url_for('auth.log_in'))
    # note = request.form.get('note')
    #
    # if len(note) < 1:
    #     flash('Note is too short!', category='error')
    # else:
    #     new_note = Note(data=note, user_id=current_user.id)
    #     db.session.add(new_note)
    #     db.session.commit()
    #     flash('Note added!', category='success')

    # return render_template("home.html", user=current_user)
    # return render_template("fuel_quote_form.html", user=current_user)
    # return render_template("fuel_quote_history.html", user=current_user)


@views.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':

        # flash('Profile created!', category='success')
        # # return redirect(url_for('views.home'))
        # return redirect(url_for('views.fuel_quote_form'))

        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        # user = User.query.filter_by(email=email).first()
        # if user:
        #     flash('Email already exists.', category='error')
        if len(full_name) < 1 or len(full_name) > 50:
            flash('Full name must be greater than 1 and less than 50 characters.', category='error')
        elif len(address1) < 2 or len(address1) > 100:
            flash('Address must be greater than 2 and less than 100 characters.', category='error')
        elif len(city) < 2 or len(city) > 100:
            flash('City must be greater than 2 and less than 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be greater than 5 and no more than 9 characters.', category='error')
        else:
            # new_user_profile = Profile(full_name=full_name, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode)
            # db.session.add(new_user_profile)
            # db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # return redirect(url_for('views.home'))
            return redirect(url_for('views.fuel_quote_form'))

    return render_template("profile.html", user=current_user)


@views.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote_form():
    if request.method == 'POST':
        return redirect(url_for("views.fuel_quote_result"))
    return render_template("fuel_quote_form.html", user=current_user)


@views.route('/fuel-quote-result', methods=['GET', 'POST'])
def fuel_quote_result():
    return render_template("fuel_quote_result.html", user=current_user)


@views.route('/fuel-quote-history', methods=['GET', 'POST'])
def fuel_quote_history():
    return render_template("fuel_quote_history.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

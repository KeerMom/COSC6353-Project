from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Profile, Quote
from . import db
import json

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('views.fuel_quote_form'))
    # return render_template("fuel_quote_form.html", user=current_user)


@views.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        if len(full_name) < 2 or len(full_name) > 50:
            flash('Full name must be greater than 2 and less than 50 characters.', category='error')
        elif len(address1) < 2 or len(address1) > 100:
            flash('Address must be greater than 2 and less than 100 characters.', category='error')
        elif len(city) < 2 or len(city) > 100:
            flash('City must be greater than 2 and less than 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be greater than 5 and no more than 9 characters.', category='error')
        else:
            print("current_user id is :", current_user.id)
            new_user_profile = Profile(full_name=full_name, address1=address1, address2=address2, city=city,
                                       state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(new_user_profile)
            db.session.commit()

            flash('Profile created!', category='success')
            #print('test')
            # return redirect(url_for('views.home'))
            return redirect(url_for('views.fuel_quote_form'))

    return render_template("profile.html", user=current_user)


@views.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote_form():
    # print("(fuel_quote) current_user id is :", current_user.id)
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    #if profile_list:
    cur_profile_id = profile_list[0].id
    # print(user.user_profile, user.email)
    # user_address = user.user_profile.address1 + user.user_profile.address2 + user.user_profile.city
    # user_state = user.user_profile.state
    # user_profile = Profile.query.get(current_user.id)
    user_profile = Profile.query.get(cur_profile_id)
    user_address = user_profile.address1 + user_profile.address2 + user_profile.city
    user_state = user_profile.state
    print("the user's address is: ", user_address)
    print("the user's state is: ", user_state)

    if request.method == 'POST':
        request_gallons = request.form.get('gallons_requested')
        request_date = request.form.get('delivery_date')
        request_address = request.form.get('delivery_address')
        # get quote history
        quote_history = Quote.query.get(current_user.id)
        if quote_history:
            history_flag = 1
        else:
            history_flag = 0

        quote_result = get_price(user_state, history_flag, int(request_gallons))
        print("suggest price is: ", quote_result[0], "total price is: ", quote_result[1])
        global quote_info
        quote_info = [request_gallons, request_address, request_date, quote_result[0], quote_result[1]]
        flash('Suggest price created!', category='success')
        return redirect(url_for('views.fuel_quote_result'))
        # return redirect(url_for('views.fuel_quote_result', quote_info=quote_info1))
        # return redirect(url_for('views.test_fuc',x='15'))
    return render_template("fuel_quote_form.html", user=current_user, address=user_address, state=user_state)


@views.route('/fuel-quote-result', methods=['GET', 'POST'])
# def test_fuc(x):
#     print("the input is ", x)
def fuel_quote_result():
    global quote_info
    print('quote_result ', quote_info)
    if request.method == 'POST':
        # save quote result to database
        # gallons = request.form.get('gallons_requested')
        # print("test save result ", gallons)
        # address = request.form.get('delivery_address')
        # delivery_date = request.form.get('delivery_date')
        # suggest_price = request.form.get('suggest_price')
        # total_price = request.form.get('total_price')

        new_quote_result = Quote(gallons_requested=quote_info[0],
                                 delivery_address=quote_info[1],
                                 date=quote_info[2],
                                 suggest_price=quote_info[3],
                                 total_price=quote_info[4], user_id=current_user.id)
        db.session.add(new_quote_result)
        db.session.commit()

        flash('Quote result added!', category='success')
        return redirect(url_for('views.fuel_quote_form'))

    return render_template("fuel_quote_result.html", user=current_user, gallons_requested=quote_info[0],
                           delivery_address=quote_info[1], delivery_date=quote_info[2], suggest_price=quote_info[3],
                           total_price=quote_info[4])


@views.route('/fuel-quote-history', methods=['GET', 'POST'])
def fuel_quote_history():
    user = User.query.get(current_user.id)
    history_list = user.user_quote
    # print('current user id is ', current_user.id)
    # print("test the quote_history result", history_list)
    # print("test the quote_history result", history_list[0].delivery_address)
    return render_template("fuel_quote_history.html", user=current_user, history_list=history_list)


def get_price(state, request_frequent, request_gallons):
    current_price = 1.5
    profit_factor = 0.1

    if state == 'TX':
        location_factor = 0.02
    else:
        location_factor = 0.04

    if request_frequent >= 1:
        history_factor = 0.01
    else:
        history_factor = 0

    if request_gallons > 1000:
        gallon_factor = 0.02
    else:
        gallon_factor = 0.03

    margin = current_price * (location_factor - history_factor + gallon_factor + profit_factor)
    suggested_price = current_price + margin
    total_due = suggested_price * request_gallons

    results = [suggested_price, total_due]
    return results
@views.route('/Aboutus', methods=['GET', 'POST'])
def Aboutus():
    return render_template("Aboutus.html", user=current_user)


@views.route('/Assignments', methods=['GET', 'POST'])
def Assignments():
    return render_template("Assignments.html", user=current_user)
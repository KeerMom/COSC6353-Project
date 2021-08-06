import unittest
import requests
from website import views
import random
import string


class MyTestCase(unittest.TestCase):
    # Ensure login behaves correctly given the correct credential
    def test_login(self):
        # Ensure that Flask was set up correctly
        response = requests.get('http://127.0.0.1:5000/login')
        # print(response)
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        self.assertTrue('Logged in successfully!' in response.text)

    def test_not_an_user_login(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'email': 'xxx@df.com', 'password': '12345678'})
        self.assertTrue('Email does not exist.' in response.text)

    def test_wrong_password_login(self):
        response = requests.post('http://127.0.0.1:5000/login',
                                 data={'email': 'xyz@gmail.com', 'password': '123456789'})
        self.assertTrue('Incorrect password, try again.' in response.text)

    def test_home(self):
        response = requests.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        response = requests.get('http://127.0.0.1:5000/')
        # print(response)
        self.assertEqual(response.status_code, 200)


    def test_sign_up(self):
        response = requests.get('http://127.0.0.1:5000/sign-up')
        self.assertEqual(response.status_code, 200)

    def test_correct_sign_up(self):
        # printing lowercase
        letters = string.ascii_lowercase
        email = ''.join(random.choice(letters) for i in range(10)) + '@gmail.com'
        response = requests.post('http://127.0.0.1:5000/sign-up',
                                 data={'email': email, 'firstName': 'ppp', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Account created!' in response.text)

    def test_exist_email_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/sign-up',
                                 data={'email': 'xyz@gmail.com', 'firstName': 'ppp', 'password1': '12345678',
                                       'password2': '12345678'})
        self.assertTrue('Email already exists.' in response.text)

    def test_password_not_match_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/sign-up',
                                 data={'email': 'aaaxxx@gmail.com', 'firstName': 'ppp', 'password1': '12345678',
                                       'password2': '123456789'})
        # print(response.text)
        self.assertTrue('Passwords don&#39;t match.' in response.text)

    def test_password_too_short_sign_up(self):
        response = requests.post('http://127.0.0.1:5000/sign-up',
                                 data={'email': 'aaa@gmail.com', 'firstName': 'ppp', 'password1': '123',
                                       'password2': '123'})
        self.assertTrue('Password must be at least 7 characters.' in response.text)

    def test_logout(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})

        response = s.get('http://127.0.0.1:5000/logout')
        # print(response)
        self.assertEqual(response.status_code, 200)

    def test_create_profile(self):
        response = requests.get('http://127.0.0.1:5000/create-profile')
        self.assertEqual(response.status_code, 200)

    def test_post_create_profile(self):
        s = requests.Session()
        # printing lowercase
        letters = string.ascii_lowercase
        email = ''.join(random.choice(letters) for i in range(10)) + '@gmail.com'
        response = s.post('http://127.0.0.1:5000/sign-up',
                          data={'email': email, 'firstName': 'ppp', 'password1': '12345678',
                                'password2': '12345678'})
        # print(response)
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/create-profile',
                          data={'fullname': fullname, 'address1': 'ppp', 'address2': '123',
                                'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        # print(response)
        self.assertTrue('Profile created!' in response.text)

    def test_full_name_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/create-profile',
                                 data={'fullname': 'x', 'address1': 'ppp', 'address2': '123',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('Full name must be greater than 2 and less than 50 characters.' in response.text)

    def test_address_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/create-profile',
                                 data={'fullname': 'xmnnc', 'address1': 'p', 'address2': '123',
                                       'city': 'acb', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('Address must be greater than 2 and less than 100 characters.' in response.text)

    def test_city_too_short_profile(self):
        response = requests.post('http://127.0.0.1:5000/create-profile',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'a', 'state': 'TX', 'zipcode': '7777777'})
        self.assertTrue('City must be greater than 2 and less than 100 characters.' in response.text)

    def test_state_not_two_profile(self):
        response = requests.post('http://127.0.0.1:5000/create-profile',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'abc', 'state': 'TXMS', 'zipcode': '7777777'})
        self.assertTrue('Reselect state.' in response.text)

    def test_zipcode_not_correct_profile(self):
        response = requests.post('http://127.0.0.1:5000/create-profile',
                                 data={'fullname': 'xmnnc', 'address1': 'pxts', 'address2': '123',
                                       'city': 'abc', 'state': 'TX', 'zipcode': '77'})
        self.assertTrue('Zipcode must be greater than 5 and no more than 9 characters.' in response.text)

    def test_get_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_form(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'gallons_requested': '100', 'delivery_date': '2021-07-08',
                                'delivery_address': 'xysdgahdgsahd, FL'})
        # print(response.txt)
        self.assertTrue('Suggest price created!' in response.text)

    def test_first_post_fuel_quote_form(self):
        s = requests.Session()
        # s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        letters = string.ascii_lowercase
        email = ''.join(random.choice(letters) for i in range(10)) + '@gmail.com'
        response = s.post('http://127.0.0.1:5000/sign-up',
                          data={'email': email, 'firstName': 'ppp', 'password1': '12345678',
                                'password2': '12345678'})
        # print(response)
        fullname = ''.join(random.choice(letters) for i in range(5))
        response = s.post('http://127.0.0.1:5000/create-profile',
                          data={'fullname': fullname, 'address1': 'xysdgahd', 'address2': 'gsah',
                                'city': 'xyz', 'state': 'TX', 'zipcode': '7777777'})
        response = s.post('http://127.0.0.1:5000/fuel-quote',
                          data={'gallons_requested': '1050', 'delivery_date': '2021-07-08',
                                'delivery_address': 'xysdgahdgsahxyz, TX'})
        # print(response.txt)
        self.assertTrue('Suggest price created!' in response.text)

    def test_get_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'gallons_requested': '100', 'delivery_date': '2021-07-08',
                     'delivery_address': 'xysdgahdgsahd, FL'})

        response = s.get('http://127.0.0.1:5000/fuel-quote-result')
        self.assertEqual(response.status_code, 200)

    def test_post_fuel_quote_result(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        s.post('http://127.0.0.1:5000/fuel-quote',
               data={'gallons_requested': '100', 'delivery_date': '2021-07-08',
                     'delivery_address': 'xysdgahdgsahd, FL'})

        response = s.post('http://127.0.0.1:5000/fuel-quote-result')
        self.assertTrue('Quote result added!' in response.text)

    def test_get_fuel_history(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/login', data={'email': 'xyz@gmail.com', 'password': '12345678'})
        response = s.get('http://127.0.0.1:5000/fuel-quote-history')
        self.assertEqual(response.status_code, 200)

    def test_get_price_tx(self):
        state = 'TX'
        request_frequent = 1
        request_gallons = 1500

        true_value = 1.695
        results = views.get_price(state, request_frequent, request_gallons)
        self.assertEqual(results[0], true_value)

    def test_get_price_not_tx(self):
        state = 'CA'
        request_frequent = 0
        request_gallons = 100

        true_value = 1.755
        results = views.get_price(state, request_frequent, request_gallons)
        self.assertEqual(results[0], true_value)

    def test_Aboutus(self):
        response = requests.get('http://127.0.0.1:5000/Aboutus')
        self.assertEqual(response.status_code, 200)

    def test_Assignments(self):
        response = requests.get('http://127.0.0.1:5000/Assignments')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

# django-shop-app
This is a store website programmed using the django freamwork and python.

Some features of this website:
1. Add product to cart
2. Has a payment gateway
3. Show products
4. Checkout page
5. Upload images for products
6. Users sign in
7. User registration
8. User registration with Google account
9. And other features...

Important note:
For payment operation you must config views.py at this address: website/shop/views.py line 61 to 64 as below:

1. MERCHANT = 'your marchant code'
2. ZP_API_REQUEST = 'https://example.com/payment-gateway-name/api.payment-gateway-name/pg/v4/payment/request.json'
3. ZP_API_VERIFY = 'https://example.com/payment-gateway-name/api.payment-gateway-name/pg/v4/payment/verify.json'
4. ZP_API_STARTPAY = 'https://example.com/payment-gateway-name/api.payment-gateway-name/pg/StartPay/{authority}'

For sending email you must config settings.py at this address: website/settings.py line 170 to 171 as below:

1. EMAIL_HOST_USER = 'youremail@gmail.com'
2. EMAIL_HOST_PASSWORD = 'your gmail app password'
3. For to implement this project you must create a virtual environment on this project
4. And install all the requirements through the requirements file with this command: pip install -r requirements.txt

Images project:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img1.png)


Cart image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img2.jpg)


Login before payment image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img3.jpg)


Checkout image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img4.jpg)


Order detail image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img5.jpg)


User sign in image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img6.jpg)


User sign up image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img7.jpg)


User sign out image:

![Website image](https://github.com/hamedkalhor76/django-shop-app/blob/main/images/img8.jpg)

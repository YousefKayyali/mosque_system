from django.contrib.auth.models import Users
from django.contrib.auth.hashers import check_password

user = Users.objects.get(profile=8)
plain_text_password_attempt = "naem123"

if check_password(plain_text_password_attempt, user.password):
    print("Password is correct.")
else:
    print("Incorrect password.")
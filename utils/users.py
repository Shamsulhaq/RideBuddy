import re
import itertools
import string
import random
from django.contrib.auth import get_user_model

User = get_user_model()

def username_validator(username):
    from django.contrib.auth import get_user_model

    User = get_user_model() 
    return not User.objects.filter(username=username).exists()

def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def clean_username():
    users = User.objects.filter(role="customer")
    for user in users:
        username = re.sub(r'[^A-Za-z0-9\s@-]', '', user.username)
        if username_validator(username):
            username = username
        else:
            username = random_string_generator()
        user.username = username
        user.set_password(username)
        user.save()
        print(f"changed {username}")
    print("Done")
    

def generate_usernames(name):
    # Split the name into words
    name = re.sub(r'[^A-Za-z0-9\s@-]', '', name) # we allow only letters numbers and '-' '@' 
    words = name.split()
    # Generate all possible combinations of the words
    combinations = []
    for r in range(1, len(words) + 1):
        combinations.extend(itertools.permutations(words, r))
    
    # Generate usernames from combinations
    usernames = set()
    for combo in combinations:
        username = ''.join(combo).lower()[:12]
        if len(username) > 4:
            usernames.add(username)
    for username in usernames:
        if username_validator(username):
            return username
    return random_string_generator()

def generate_user(name, role=None):
    username = generate_usernames(name)
    role = role if role else 'customer'
    user = User(username=username, role=role, created_by_id=1)
    user.set_password(username)
    user.save()
    return user


def audit_user(obj):
    created_by = None
    if obj.created_by:
        created_by = User.objects.filter(username=obj.created_by).first()

    modified_by = None
    if obj.modified_by:
        modified_by = User.objects.filter(username=obj.modified_by).first()

    deleted_by = None
    if obj.deleted_by:
        deleted_by = User.objects.filter(username=obj.deleted_by).first()

    return created_by, modified_by, deleted_by
    

                
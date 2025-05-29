import json
from django.utils import timezone


def server_time():
    now = timezone.now()
    now = timezone.localtime(now)
    return now


def request_to_dict(request):
    # This method will return Dict Data from request.Meta
    return {i[0]: i[1] for i in request.META.items() if i[0].startswith('HTTP_')}


def json_loaded_data(string):
    """ this method is for get json response whatever """
    try:
        data = json.loads(string)
    except:
        if type(string) == str:
            _str = string.replace("'", '"')
            data = json.loads(_str)
        else:
            data = string
    return data

def get_year_choices():
    current_year = timezone.now().year
    return [(year, str(year)) for year in range(1971, current_year + 1)]

def get_number_choices(first_number=1, last_number=99):
    """
    Optionally takes two arguments: first_number, last_number, and returns list of numbers between these (inclusive).
    Default to 1-99
    """
    return [(num, str(num)) for num in range(first_number, last_number+1)]


    
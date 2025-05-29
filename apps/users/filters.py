from django_filters import rest_framework as filters
from utils.filters import BaseOrderBy
from .models import User


class UserFilter(BaseOrderBy):
    date_joined = filters.DateFilter(field_name='date_joined__date') 
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')
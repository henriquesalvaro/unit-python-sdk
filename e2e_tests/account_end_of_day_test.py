import os
import unittest
from unit import Unit
from unit.models.account_end_of_day import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_account_end_of_day():
    params = AccountEndOfDayListParams(10, 0, "", "49430")
    response = client.account_end_of_day.list(params)
    for a in response.data:
        assert a.type == "accountEndOfDay"

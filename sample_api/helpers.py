import datetime

from django.db.models import Sum


def str_to_datetime(date_str, format='%d.%m.%Y'):
    """
    Convert string date to datetime
    params:
        date_str: string date i.e. 17.05.2017
        format: default format is %d.%m.%Y
    Return: date object or None
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, format)
        return date_obj.date()
    except:
        return None


def get_sum_annotation(aggregate_sum_list, only_aggregate=False):
    """
    return: annotation dict for sum only i.e. {"clicks": Sum("clicks")}
    As per need we can extend annotation features i.e. Avg, Count
    """
    sum_annotation = {}
    for key in aggregate_sum_list:
        sum_annotation.update({
            key + '_sum' if only_aggregate else key: Sum(key),
        })
    return sum_annotation


def get_date_filter(date_str, date_lte, date_gte, date_from, date_to, month, year):
    """
    return date filter as per give dates
    i.e:
    {'date__year': 2017, 'date__month': 6, 'date__day': 1}
    {'date__lte': datetime.date(2017, 6, 1)}
    {'date__gte': datetime.date(2017, 6, 1)}
    {'date__year': '2017', 'date__month': '5'}
    """
    date_filter = {}
    if date_str:
        # check for single day or whole month filter
        date_obj = str_to_datetime(date_str)
        if date_obj:
            date_filter = {
                'date__year': date_obj.year,
                'date__month': date_obj.month,
            }
            if date_obj.day:
                date_filter.update({
                    'date__day': date_obj.day
                })

    elif date_lte:
        date_obj = str_to_datetime(date_lte)
        if date_obj:
            date_filter = {
                "date__lte": date_obj
            }
    elif date_gte:
        date_obj = str_to_datetime(date_gte)
        if date_obj:
            date_filter = {
                "date__gte": date_obj
            }
    elif date_from and date_to:
        date_from_obj = str_to_datetime(date_from)
        date_to_obj = str_to_datetime(date_to)
        if date_from_obj and date_to_obj:
            date_filter = {
                'date__gte': date_from_obj,
                'date__lte': date_to_obj
            }
    elif month and year:
        date_filter = {
            'date__year': year,
            'date__month': month
        }
    elif year:
        date_filter = {
            'date__year': year,
        }
    return date_filter


def add_other_filters(_filter, channel, country, os):
    """
    Other filters for API
    """
    if channel:
        _filter.update({
            'channel': channel
        })
    if country:
        _filter.update({
            'country': country
        })
    if os:
        _filter.update({
            'os': os
        })

import csv
import datetime

from django.conf import settings
from django.db.models import FloatField, F, Sum
from django.http import JsonResponse

from .models import AdvertisingData
from .helpers import get_date_filter, get_sum_annotation, add_other_filters

allowed_fields = {'id', 'date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue', 'cpi'}


def get_advertising_data(request):

    _filter = {}
    date_str = request.GET.get('date', '')
    date_lte = request.GET.get('date_lte', '')
    date_gte = request.GET.get('date_gte', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')

    # example date format: date_str = '17.05.2017'
    # date filter
    date_filter = get_date_filter(date_str, date_lte, date_gte, date_from, date_to, month, year)
    _filter.update(date_filter)

    # other filter
    channel = request.GET.get('channel', '')
    country = request.GET.get('country', '')
    os = request.GET.get('os', '')
    cpi = request.GET.get('cpi', 0)
    # add channel, country and os filter
    add_other_filters(_filter, channel, country, os)

    # Group by
    group_by_ = request.GET.get('group_by', '')
    group_by = [group for group in group_by_.split(',') if group in allowed_fields]

    # Aggregate Sum
    aggregate_sum = request.GET.get('aggregate_sum', '')
    aggregate_sum_list = [aggr_sum for aggr_sum in aggregate_sum.split(',') if aggr_sum in allowed_fields]

    # get order params
    ordering = request.GET.get('ordering', '')

    # get queryset for models
    queryset = AdvertisingData.objects.filter(**_filter)

    # import pdb;pdb.set_trace()

    # CPI calculation, aggregate_sum, annotate
    if group_by and int(cpi):
        queryset = queryset.values(*tuple(group_by)).annotate(
            spend_sum=Sum(
                'spend',
                output_field=FloatField()
            ),
            installs_sum=Sum(
                'installs',
                output_field=FloatField()
            )
        ).annotate(
            cpi=F('spend_sum') / F('installs_sum')
        )
    elif group_by and aggregate_sum:
        queryset = queryset.values(*tuple(group_by)).annotate(**get_sum_annotation(aggregate_sum_list)).order_by()
    elif aggregate_sum:
        queryset = queryset.values().annotate(**get_sum_annotation(aggregate_sum_list, only_aggregate=True)).order_by()
    elif group_by:
        queryset = queryset.values(*tuple(group_by)).order_by()
    else:
        queryset = queryset.values()

    # set default ordering if not match in fields
    if not ordering.lstrip("-") in allowed_fields:
        ordering = 'id'
    queryset = queryset.order_by(ordering)

    print(queryset.query)
    print(ordering)

    return JsonResponse(dict(data=list(queryset)))


def import_db(request):
    """
    Ignore this snippet, it's just for import date from csv to models
    """
    with open(settings.BASE_DIR + '/sample_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print('Column names are {", ".join(row)}')
                line_count += 1
            else:
                print('\t{row[0]} -- {row[1]} -- {row[2]}')
                date_obj = datetime.datetime.strptime(row[0], '%d.%m.%Y')
                AdvertisingData.objects.get_or_create(
                    date=date_obj.date() if date_obj else date_obj,
                    channel=row[1],
                    country=row[2],
                    os=row[3],
                    impressions=int(row[4]),
                    clicks=int(row[5]),
                    installs=int(row[6]),
                    spend=float(row[7]),
                    revenue=float(row[8]),
                )
                line_count += 1
        print('Processed {line_count} lines.')
    return JsonResponse({"success": True})

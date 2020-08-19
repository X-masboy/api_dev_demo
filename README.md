# API

1) Filter by time range (date_from / date_to is enough), channels, countries, operating systems
2) Group by one or more columns: date, channel, country, operating system
2) Sort by any column in ascending or descending order


### Prerequisites


```
- Docker CE
- Python3
```

### Installing

A step by step series of examples that tell you how to get a development env running

```
git clone https://github.com/amitvadhel/api_dev.git

---------------------------------------
-> Using docker:
---------------------------------------

docker-compose build
docker-compose up

Default database is sqlite3
** Intentionally I pushed db.sqlite3, to avoid migration and data import.

If you want to use PostgreSQL (Optional):

    You have uncomment the PostgreSQL driver from settings.py

    Run migrations:
        docker-compose run web python /code/manage.py migrate --noinput

    Import data:
        http://localhost:8080/import_db
        It may take some time.

---------------------------------------
-> Without docker
---------------------------------------
1) Create venv -> virtualenv -p python3 .venv
2) Enable virtualenv -> source .venv/bin/activate
3) Install requirements -> pip install requirements.txt
4) Run django -> python manage.py runserver 0.0.0.0:8080

```

## HTTP GET API endpoint example

Solution for given use cases:

1) Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.

Solution:
```
http://localhost:8080/api/sample/?date_lte=01.06.2017&group_by=channel,country&aggregate_sum=impressions,clicks&ordering=-clicks

O/P:
{'data': [{'channel': 'adcolony',
           'clicks': 13089,
           'country': 'US',
           'impressions': 532608},
          {'channel': 'apple_search_ads',
           'clicks': 11457,
           'country': 'US',
           'impressions': 369993},
          {'channel': 'vungle',
           'clicks': 9430,
           'country': 'GB',
           'impressions': 266470},
          {'channel': 'vungle',
           'clicks': 7937,
           'country': 'US',
           'impressions': 266976},
          {'channel': 'unityads',
           'clicks': 7374,
           'country': 'US',
           'impressions': 215125},
          {'channel': 'facebook',
           'clicks': 6282,
           'country': 'DE',
           'impressions': 214725},
          {'channel': 'google',
           'clicks': 6252,
           'country': 'US',
           'impressions': 211378}]
           ......
}
```

2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

Solution:
```
http://localhost:8080/api/sample/?year=2017&month=5&os=ios&group_by=date&aggregate_sum=installs&ordering=date

O/P:
{'data': [{'date': '2017-05-17', 'installs': 755},
          {'date': '2017-05-18', 'installs': 765},
          {'date': '2017-05-19', 'installs': 745},
          {'date': '2017-05-20', 'installs': 816},
          {'date': '2017-05-21', 'installs': 751},
          {'date': '2017-05-22', 'installs': 781},
          {'date': '2017-05-23', 'installs': 813},
          {'date': '2017-05-24', 'installs': 789},
          {'date': '2017-05-25', 'installs': 875},
          {'date': '2017-05-26', 'installs': 725},
          {'date': '2017-05-27', 'installs': 712},
          {'date': '2017-05-28', 'installs': 664},
          {'date': '2017-05-29', 'installs': 752},
          {'date': '2017-05-30', 'installs': 762},
          {'date': '2017-05-31', 'installs': 685}]
}

```

3) Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

Solution:
```
http://localhost:8080/api/sample/?date=01.06.2017&country=US&group_by=os&aggregate_sum=revenue&ordering=-revenue

O/P:
{"data": [{"os": "android", "revenue": 1205.21}, {"os": "ios", "revenue": 398.87}]}
```

4) Add CPI (cost per install) metric that is calculated as cpi = spend / installs. Use case: show CPI values for Canada (CA) broken down by channel ordered by CPI in descending order. Please think creafully which is an appropriate aggregate function for CPI.

Solution:
```
http://localhost:8080/api/sample/?cpi=1&country=CA&group_by=channel&ordering=-cpi

O/P:
{'data': [{'channel': 'facebook',
           'cpi': 2.0748663101604277,
           'installs_sum': 561.0,
           'spend_sum': 1164.0},
          {'channel': 'chartboost',
           'cpi': 2.0,
           'installs_sum': 637.0,
           'spend_sum': 1274.0},
          {'channel': 'unityads',
           'cpi': 2.0,
           'installs_sum': 1321.0,
           'spend_sum': 2642.0},
          {'channel': 'google',
           'cpi': 1.7419860627177708,
           'installs_sum': 574.0,
           'spend_sum': 999.9000000000004}]
}

```

5) Filter the records from 24.05.2017 to 13.06.2017, ordered by date desc.

Solution:
```
http://localhost:8080/api/sample/?date_from=24.05.2017&date_to=13.06.2017&ordering=-date

```

6) Total installs occurred in 2017 at Germany[DE], broken down by os, sorted by installs in ascending order

Solution:
```
http://localhost:8080/api/sample/?year=2017&country=DE&group_by=os&aggregate_sum=installs&ordering=installs

O/P:
{"data": [{"os": "android", "installs": 2116}, {"os": "ios", "installs": 2362}]}
```

7) Show CPI values for USA (US) broken down by os ordered by CPI in descending order.

Solution:
```
http://localhost:8080/api/sample/?cpi=1&country=US&group_by=os&ordering=-cpi

O/P:
{"data": [{"os": "android", "spend_sum": 16322.429999999995, "installs_sum": 8344.0, "cpi": 1.9561876797698938}, {"os": "ios", "spend_sum": 22522.470000000005, "installs_sum": 11606.0, "cpi": 1.9405884887127351}]}
```


Filter usage:
```
	date:
		- For specific date use filter like this --> date=17.05.2017
		- Date range usage --> date_from=17.05.2017&date_to=28.05.2017
		- lte --> date_lte 22.05.2017
		- gte --> date_gte 22.05.2017
		- yearly --> year=2017
		- year and month --> year=2017&month=6
	os:
		- example --> os=ios
	country:
		- example --> country=DE
	channel:
		- example --> channel=facebook
```


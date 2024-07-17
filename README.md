## Introduction

This project contains some automation to analyse datadog cost based on various services

## How to get auth

1. Get datadog cookie
   1. Access https://app.datadoghq.eu/ or other URL and open developer mode
   2. open network monitor and see any request
   3. Get `Cookie` request header value
2. Add `AUTH_COOKIE` in `.env` file with cookie value which you get above.

## Various script for report generation in sqlite

### fleet.py

Generate all Datadog agent information with tags using it.



## Generate CSV from data

Run the scripts which collects all information and generate csv for it.

```
sqlite3 -header -csv <sqlite_file> "select * from <table_name>;" > out.csv
```

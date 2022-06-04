from datetime import datetime, timedelta

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
# add two hours to synchronize docker time with machine time
today = datetime.date(datetime.today() - timedelta(days = 1) + timedelta(hours=2))
today_string = datetime.strftime(today, '%Y-%m-%d')

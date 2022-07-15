import requests
location = 78 # Kathmandu DAO
dates = requests.get(f'https://emrtds.nepalpassport.gov.np/iups-api/calendars/{location}/false')
print(dates.content)
if dates.status_code == 200:
    import pandas as pd
    import datetime as dt
    usuable_dates = set(pd.date_range(dt.datetime.strptime(dates.json()['minDate'],'%Y-%m-%d'),dt.datetime.strptime(dates.json()['maxDate'],'%Y-%m-%d'),freq='d').strftime('%Y-%m-%d').tolist()) - set(dates.json()['offDates'])
    print(f'\nUsuable Dates for {location}: {list(usuable_dates)}')
    df = pd.DataFrame()
    for date in usuable_dates:
        open_time = requests.get(f'https://emrtds.nepalpassport.gov.np/iups-api/timeslots/{location}/{date}/false')
        o_df = pd.DataFrame(open_time.json())
        o_df['date'] = date
        o_df['location'] = location
        df = df.append(o_df)
    print(df)
else:
    print(dates.status_code)

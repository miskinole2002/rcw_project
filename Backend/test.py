from datetime import datetime
from dateutil.relativedelta import relativedelta

current_time=datetime.now()
future_tinme=current_time+ relativedelta(years=1)
begin_date=current_time.strftime("%d-%m-%y")
end_date=future_tinme.strftime("%d-%m-%y")

print(f"la date de debut est {begin_date}")
print(f"la date de fin est {end_date}")

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

checkin = pd.read_csv('/Users/casita/stats.csv')

#display(checkin.head(8))
#display(checkin.info())

checkin = checkin.assign(date_dt = pd.to_datetime(checkin['date'],format='%Y-%m-%d'))

#display(checkin.info())
#display(checkin.head(5))

#convert to long from wide
checkin2 = checkin.melt(id_vars=['date_dt'], value_vars=['ghfc','trial','psfc','cbfc','visitor'], var_name='shopper_type', value_name='shopper_count').reset_index()

checkin2.info()
checkin2.head(4)

#%%
import seaborn as sns

#group by week and display
#datetime.dt.to_period week starts on a Monday
checkin_weekly = (
    checkin2
    .assign(week_start=checkin2['date_dt'].dt.to_period('W').dt.start_time)
    .groupby(['week_start', 'shopper_type'])['shopper_count']
    .sum()
    .reset_index()
)

checkin_weekly.info()
display(checkin_weekly.head(4))

#%%
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x='week_start', y='shopper_count', hue='shopper_type', data=checkin_weekly, ax=ax)
ax.set_title('Weekly shopping visits by shopper type (check-in desk)')
ax.set_xlabel('Year week')
ax.set_ylabel('Shopper count')
plt.show()
'''

#%%

#identify the the last full week that would have been recorded (end of the previous week)

from datetime import datetime, timedelta

print(datetime.now().date())

#0 = Monday convention
int_to_subtract = datetime.now().weekday() + 1 

#this date filter would represent the minimum date to query, and so set it as  WHERE date > prev_week_start
prev_week_start = datetime.now() - timedelta(days=int_to_subtract)



# %%

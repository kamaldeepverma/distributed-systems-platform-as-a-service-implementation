from datetime import datetime,date



def merge_service(record):
    record=record.split(',')
    cname=record[2]+' '+record[3]
    record[13]=cname
    record=','.join(record)
    calculation_service(record)

def calculation_service(record):
    record=record.split(',')
    date_format = "%Y-%m-%d"
    today=date.today()
    today_date_format = datetime.today().strftime('%Y-%m-%d')
    prime_expiry_date=record[11]
    
    born=datetime.strptime(record[4], date_format)

    prime_days_left = datetime.strptime(prime_expiry_date, date_format) - datetime.strptime(today_date_format, date_format) 
    
    age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    
    record[15]=str(prime_days_left.days)
    record[14]=str(age)
    record=','.join(record)
    conversion_service(record)

def conversion_service(record):
    print(record)
'''
Currency conversion
pip install --user currencyconverter
from currency_converter import CurrencyConverter
c = CurrencyConverter()
c.convert(100, 'EUR', 'USD')
c.convert(100, 'EUR') #default is EURO
100.0
c.convert(100, 'USD') # doctest: +SKIP
72.67

Timezone conversion

saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/
sudo easy_install --upgrade pytz
'''
    


record="1,c100,kamaldeep,verma,1994-07-01,smartwatch,25,accessories,2017-07-23 13:10:11,2017-07-25 13:10:11,USD,2020-08-23,IST"
for i in range(5):
    record=record+',NC'

# record=record.split(',')
merge_service(record)
# print(record)

# 0 Order_number
# 1 Customer_id
# 2 Customer_fname
# 3 Customer_lname
# 4 Date_of_birth
# 5 Product_name
# 6 Product_price
# 7 Product_category
# 8 Order_timestamp
# 9 Delivery_timestamp
# 10 Currency_format
# 11 Prime_membership_expiry_date
# 12 Time_zone
# 13 Customer_name
# 14 Age
# 15 Prime_expiry_days_left
# 16 Standard_price 
# 17 UTC_timestamp




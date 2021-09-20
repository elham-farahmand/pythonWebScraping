import re
from bs4 import BeautifulSoup
import requests
import mysql.connector

car_model = input('Insert the car name: ')

res = requests.get('https://www.truecar.com/used-cars-for-sale/listings/' + car_model)
soup = BeautifulSoup(res.text, 'html.parser')

price = soup.find_all('div', attrs = {'data-test':'vehicleListingPriceAmount'})
mileage = soup.find_all('div', attrs = {'data-test':'vehicleMileage'})

price_result = re.findall(r'\"vehicleCardPricingBlockPrice\"\>(.*?)\<\/div\>' , str(price))
mileage_result = re.findall(r'svg\>(.*?)\<\!-- --\> miles' , str(mileage))

dbname = 'truecar'
tablename = 'car'
cnx = mysql.connector.connect(user = 'root', password = '', host = '127.0.0.1', database = dbname)
cursor = cnx.cursor()

count = 0
for item in price_result:
    count+=1
    if ( count <= 20):
        cursor.execute('INSERT INTO %s VALUES (\'%s\',\'%s\')' % (tablename, price_result[count], mileage_result[count]))
    else:
        break

cnx.commit()
cnx.close()
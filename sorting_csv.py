import pandas as pd 
import random

cars = pd.read_csv('Cars.csv', index_col=0)

pd.set_option('max_colwidth', 500) 
#input_region = input('Введіть регіон: ')
#input_price = input('Введіть ціну: ')
#input_transmition = input('Введіть трансмісію: ')

#print(cars)
#print(cars['price_usd'].dtype)

#print(cars.groupby('region').region.count())


def create_region_csv(region):


    def input_region(cars, region):

        cars = pd.read_csv('Cars.csv', index_col=0)
        
        cars_by_region = cars.loc[cars['region'] == region]

        return cars_by_region

    def create_csv(region = input_region(cars, region)):

        region.to_csv('Cars_by_region.csv')

def input_things(input_region):
    

    return input_region, input_price, input_transmition

input_region, input_price, input_transmition = input_things()

def replaced_price(input_price):

    input_price = input_price.rsplit('-')
    price = []
    for item in input_price:
        price.append(int(item.strip()))

    return price

price = replaced_price(input_price)

def sort_cars(cars, region, price, transmition):
    
    user_cars = cars.loc[(cars['region'] == region) & (cars['price_usd'] >= price[0]) & (cars['price_usd'] <= price[-1]) & (cars['transmition'] == transmition)]
    
    return user_cars

user_cars = sort_cars(cars, input_region, price, input_transmition)

def convert_csv(cars):

    cars.to_csv('user_cars.csv')

while user_cars.empty == True:
    input_things()
    user_cars =  sort_cars(cars, input_region, price, input_transmition)
else:
    convert_csv(user_cars)
    user_cars = pd.read_csv('user_cars.csv')
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from covid import Covid
import locale
from pathlib import Path
from chatterbot.response_selection import get_random_response
from pprint import pprint
from re import search
from flask import Flask, request
import spacy
from spacy.cli.download import download
download(model="en")

app = Flask(__name__)

script_location = Path(__file__).absolute().parent
locale.setlocale(locale.LC_ALL, 'en_US')

covid = Covid(source="worldometers")


def get_country(text):

    '''
    FROM USER INPUT,
    WE GET THE COUNTRY MENTIONED
    '''
    countries = []
    countries_location = script_location / 'countries.txt'
    data = open(countries_location).readlines()
    for x in data:
        countries.append(x.strip().lower())
    
    for country in countries:
        if country in text:
            return country
 

def get_corona_stats(country):

    active = (covid.get_status_by_country_name(country)['active'])
    confirmed = (covid.get_status_by_country_name(country)['confirmed'])
    recovered = (covid.get_status_by_country_name(country)['recovered'])
    deaths = (covid.get_status_by_country_name(country)['deaths'])

    active = locale.format_string("%d", active, grouping=True)
    confirmed = locale.format_string("%d", confirmed, grouping=True)
    recovered = locale.format_string("%d", recovered, grouping=True)
    deaths = locale.format_string("%d", deaths, grouping=True)

    response_is = 'For {}, active cases are: {}, total confirmed cases are: {}, total recovered is: {}, total deaths (rest in pease) is {}'.format(
        country, active, confirmed, recovered, deaths)
    return response_is


def user_ask_about_corona(text):
    '''
    RETURNS TRUE, IF THERE ARE KEY WORDS IN WHAT USER ASKS
    TO CHECK IF WE WANT TO CHECK FOR CORONA CASES
    '''

    words_to_check = ['corona', 'covid',
                               'covid19', 'covid19', 'corona virus', 'cases','Corona','Covid','Covid19']

    return any(x in text for x in words_to_check)

def get_corona_world_stats():
    active = covid.get_total_active_cases()
    confirmed = covid.get_total_confirmed_cases()
    recovered = covid.get_total_recovered()
    deaths = covid.get_total_deaths()

    active = locale.format_string("%d", active, grouping=True)
    confirmed = locale.format_string("%d", confirmed, grouping=True)
    recovered = locale.format_string("%d", recovered, grouping=True)
    deaths = locale.format_string("%d", deaths, grouping=True)

    response_is = 'For the ENTIRE WORLD, total active cases are: {}, total confirmed cases are: {}, total recovered is: {}, total deaths (rest in pease) is {}'.format(
        active, confirmed, recovered, deaths)
    return response_is

# if running local uncomment line below
@app.route('/')
def chatbot():
    print('beginning')
    message = (request.args.get('message'))
    # response = get_bot_response(message)
    print('end')

    return message




# Get a response to an input statement
def get_bot_response(inquiry):
    chatbot = ChatBot(
        "ChatBot", response_selection_method=get_random_response,

        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'my programming isnt the best, I didnt understand that last part lol '
            },
            'chatterbot.logic.MathematicalEvaluation',
        ],
        storage_adapter="chatterbot.storage.SQLStorageAdapter",

    )

    # Create a new trainer for the chatbot
    # show_training_progress=False
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('./sad.yml')
    inquiry = str(inquiry).lower()
    response = 'kk'
    cntry=''
    if user_ask_about_corona(inquiry):
        cntry = get_country(inquiry)
        if cntry == None:
            response = get_corona_world_stats()
        else:
            response = get_corona_stats(cntry.lower())

    else:
        response = chatbot.get_response(inquiry)

    return str (response)

if __name__ == "__main__":
    app.run()
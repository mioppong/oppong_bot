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

covid = Covid(source="worldometers")


def get_country(text):

    '''
    FROM USER INPUT,
    WE GET THE COUNTRY MENTIONED
    '''
    countries = ['north america', 'asia', 'south america', 'europe', 'africa', 'oceania', 'world', 'usa', 'india', 'brazil', 'russia', 'spain', 'argentina', 'colombia', 'france', 'peru', 'mexico', 'uk', 'south africa', 'iran', 'chile', 'iraq', 'italy', 'bangladesh', 'germany', 'indonesia', 'philippines', 'turkey', 'saudi arabia', 'pakistan', 'israel', 'ukraine', 'netherlands', 'belgium', 'canada', 'romania', 'poland', 'morocco', 'czechia', 'ecuador', 'bolivia', 'nepal', 'qatar', 'panama', 'dominican republic', 'kuwait', 'uae', 'oman', 'kazakhstan', 'egypt', 'sweden', 'guatemala', 'portugal', 'costa rica', 'japan', 'ethiopia', 'belarus', 'honduras', 'venezuela', 'bahrain', 'switzerland', 'moldova', 'austria', 'armenia', 'uzbekistan', 'lebanon', 'nigeria', 'singapore', 'algeria', 'paraguay', 'kyrgyzstan', 'ireland', 'libya', 'ghana', 'palestine', 'hungary', 'azerbaijan', 'kenya', 'tunisia', 'afghanistan', 'jordan', 'serbia', 'myanmar', 'denmark', 'bosnia and herzegovina', 'el salvador', 'slovakia', 'bulgaria', 'australia', 'croatia', 'greece', 's. korea', 'north macedonia', 'cameroon', 'malaysia', 'ivory coast', 'georgia', 'albania', 'madagascar', 'norway', 'zambia', 'montenegro', 'senegal', 'sudan', 'finland', 'slovenia', 'namibia', 'guinea', 'maldives', 'drc', 'luxembourg', 'mozambique', 'uganda', 'tajikistan', 'french guiana', 'haiti', 'gabon', 'jamaica', 'zimbabwe', 'cabo verde', 'mauritania', 'lithuania', 'angola', 'guadeloupe', 'cuba', 'malawi', 'eswatini', 'bahamas', 'sri lanka', 'djibouti', 'nicaragua', 'trinidad and tobago', 'hong kong', 'botswana', 'congo', 'suriname', 'equatorial guinea', 'syria', 'rwanda', 'car', 'réunion', 'malta', 'aruba', 'estonia', 'iceland', 'mayotte', 'somalia', 'french polynesia', 'guyana', 'thailand', 'gambia', 'latvia', 'mali', 'andorra', 'south sudan', 'belize', 'cyprus', 'uruguay', 'benin', 'guinea-bissau', 'burkina faso', 'sierra leone', 'martinique', 'yemen', 'togo', 'new zealand', 'lesotho', 'chad', 'liberia', 'niger', 'vietnam', 'sao tome and principe', 'san marino', 'sint maarten', 'channel islands', 'curaçao', 'diamond princess', 'turks and caicos', 'papua new guinea', 'gibraltar', 'burundi', 'taiwan', 'saint martin', 'tanzania', 'comoros', 'faeroe islands', 'eritrea', 'mauritius', 'isle of man', 'bhutan', 'mongolia', 'cambodia', 'monaco', 'cayman islands', 'liechtenstein', 'barbados', 'bermuda', 'caribbean netherlands', 'seychelles', 'brunei', 'antigua and barbuda', 'st. barth', 'british virgin islands', 'st. vincent grenadines', 'macao', 'dominica', 'saint lucia', 'fiji', 'timor-leste', 'grenada', 'vatican city', 'new caledonia', 'laos', 'saint kitts and nevis', 'greenland', 'saint pierre miquelon', 'montserrat', 'falkland islands', 'western sahara', 'ms zaandam', 'anguilla', 'solomon islands', 'wallis and futuna', 'china']

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
    response = get_bot_response(message)
    print('end')

    return response




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
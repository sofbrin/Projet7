#! /usr/bin/env python
# coding: utf8

import re
import string
import wikipedia
from gpbapp.utils.stopwords import stopwords
import googlemaps
from datetime import datetime
from settings import API_KEY


class GrandpyAnswer:

    def __init__(self, question):
        self.question = question
        self.gmaps = googlemaps.Client(key=API_KEY)

    def questionParser(self):
        """ parse the user's question """
        parsed_words = []
        # 1. remove punctuation
        remove_punctuation = re.sub(r'[^\w\s]',' ', self.question)
        # 2. remove capitals
        capitals_free = remove_punctuation.lower()
        # 3. remove spaces
        split_question = capitals_free.split()
        # 4. parse question
        for word in split_question:
            if word not in stopwords:
                parsed_words.append(word)
        parsed_question = ' '.join(parsed_words)
        return parsed_question


    def wikiAnswer(self, parsed_question):
        """ process the wikipedia API """
        wikipedia.set_lang("fr")
        wikiSearch = wikipedia.search(parsed_question, results=1)
        if len(wikiSearch) == 0:
            return {
                    'url': None,
                    'summary': None,
                    'search': None
            }
        else:
            wikiAnswer = wikipedia.summary(wikiSearch[0], sentences=1)
            wikiPage = wikipedia.page(wikiSearch[0])
            data = {'url': wikiPage.url,
                    'summary': wikiAnswer,
                    'search': wikiSearch[0]
            }
            return data

    def gmapAnswer(self, search):
        """ process the google API """
        geocode_result = self.gmaps.geocode(search, language="fr")
        if len(geocode_result) == 0:
            return {
                'address': None,
                'latitude': None,
                'longitude': None
            }
        else:
            data = {'address': geocode_result[0]['formatted_address'],
                    'latitude': geocode_result[0]['geometry']['location']['lat'],
                    'longitude': geocode_result[0]['geometry']['location']['lng']
                    }
            print(data)
            return data

    def gpbAnswer(self):
        """ bring the search's datas together """
        data_question = self.questionParser()
        if data_question == "":
            data = data_question
            return data

        else:
            try:
                data_wiki = self.wikiAnswer(data_question)
                if data_wiki['search'] is None:
                    data_gmaps = self.gmapAnswer(data_question)
                else:
                    data_gmaps = self.gmapAnswer(data_wiki['search'])
                data = {**data_wiki, **data_gmaps}
                return data

            except wikipedia.exceptions.DisambiguationError:
                return "error"

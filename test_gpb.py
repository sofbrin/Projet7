#! /usr/bin/env python
# coding: utf8

import gpbapp.grandpyAnswer as script

question = 'Est-ce que par hasard tu connais Trou aux Biches ?'
def test_questionParser():
    """ test the parser """

    parsed_question = script.GrandpyAnswer(question).questionParser()
    assert parsed_question == 'trou biches'

def test_wikiAPI(monkeypatch):
    """ test the wikipedia API """

    result = "Trou-aux-Biches est une ville de la côte Nord de l'île Maurice située dans le district de Pamplemousses."

    def mockreturn(parsed_question):
        return result

    parsed_question = "trou biches"
    monkeypatch.setattr('gpbapp.grandpyAnswer.GrandpyAnswer.wikiAnswer', mockreturn)
    apiW = script.GrandpyAnswer(parsed_question)

    assert apiW.wikiAnswer() == result

def test_gmapAPI(monkeypatch):
    """ test the google API """

    result = {
        "latitude": -20.0321,
        "longitude": 57.5504
    }

    def mockreturn(search):
        return result

    search = "trou biches"
    monkeypatch.setattr('gpbapp.grandpyAnswer.GrandpyAnswer.gmapAnswer', mockreturn)
    apiG = script.GrandpyAnswer(search[1])

    assert apiG.gmapAnswer() == result

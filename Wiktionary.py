import xml.etree.cElementTree as ET
import xml.sax
import lxml
import re
from lxml import etree
import csv
from collections import defaultdict



# =============================================================================
# Producing the wikitionary.csv Script
# =============================================================================
#
# This script produces the wikitionary.csv.
# This file is a ressource for nlp, it's a french dictionary with a language level tag for each word.
# Those tags are gathered from a xml dump of all the definitions of the french wictionary.
# To set the tag of words which have several definitions but with different language levels, it has been decided to select the tag the most mentioned through all it definitions.
# This script needs the other nlp ressource to be build.






BALISE = re.compile(r'{http://www.mediawiki.org/xml/export-0.10/}')
LANGUAGE = re.compile(r'\{\{langue\|[a-z]{2}\}\}')
EXCEPTIONS = re.compile(r':')
DEFINITION = re.compile(r"^# ")
VERB = re.compile(r'(?:Première|Deuxième|Troisième) personne du (?:singulier|pluriel) ')

hierarchy = {"level0":0, "level1":1, "level2":0, "autre":0}


def create_regex():
    regex = {}

    reg0 = re.compile(r"\{populaire[\|\}]|\[populaire\]|\{injurieux[\|\}]|\[injurieux\]|\{très familier[\|\}]|\[très familier\]|\{vulgaire[\|\}]|\[vulgaire\]|\{familier[\|\}]|\[familier\]| \{argot[\|\}]|\[argot\]|\{verlan[\|\}]|\[verlan\]")
    reg2 = re.compile(r"\{littéraire[\|\}]|\[littéraire\]|\{poétique[\|\}]|\[poétique\]|\{soutenu[\|\}]|\[soutenu\]")
    rega = re.compile(r"\{plaisanterie[\|\}]|\[plaisanterie\]|\{ironique[\|\}]|\[ironique\]|\{péjoratif[\|\}]|\[péjoratif\]|\{euphémisme[\|\}]|\[euphémisme\]|\{enfantin[\|\}]|\[enfantin\]|\{informel[\|\}]|\[informel\]")

    regex["level0"] = reg0
    regex["level2"] = reg2
    regex["autre"] = rega

    return regex

REGEX = create_regex()

def get_langage_level(definitions):
    if definitions == []:
        return "level1"
    type_def = defaultdict(int)
    nb_level1 = len(definitions)
    for definition in definitions:
        for level in REGEX.keys():
            if bool(REGEX[level].search(definition)):
                type_def[level] += 1
                nb_level1 -= 1
                break
    type_def["level1"] = nb_level1
    print("type_def",type_def)
    language_level = max(type_def.items(), key = lambda item:(item[1], hierarchy[item[0]]))
    return language_level[0]


def is_french(txt, word):
    if txt == None:
        return False
    language = re.findall(LANGUAGE,txt)
    if not language:
        return False
    if "fr" not in language[0]:

        print("                ", word)
        print(language)
        return False
    else:
        return True

def is_exception(word):
    if EXCEPTIONS.search(word) or word == "":
        return True
    else:
        return False

def get_definition(txt):
    definitions = []
    i = 0
    if txt:
        txt = txt.split("\n")
        for line in txt:
            if DEFINITION.search(line):
                if not bool(VERB.search(line)):
                    i += 1
                    print("  -",line)
                    definitions.append(line)
            if i > 5:
                break
    return definitions



def extract_language_level():
    ON_DEF = False
    VERB_DEF = False
    total_word = 0

    fd = open("wikitionary.csv", "w")
    fieldnames = ["word", "language_level"]
    writer = csv.DictWriter(fd, fieldnames=fieldnames)
    writer.writeheader()


    title = ""
    nb_word = 0

    context = ET.iterparse("wikitionary.xml", events=("start", "end"))
    context = iter(context)

    event, root = next(context)

    i = 0
    k = 0

    for event, elem in context:
        tag = BALISE.sub("",elem.tag)
        value = elem.text
        if event == "start":
            if tag == "page":
                language_level = ""
                #print("NEW PAGE")
                i+ = 1
            elif tag == "text":
                #print("begin text")
                i+ = 1

        elif event == "end":

            if tag == "page":
                if WORD == True:
                    new_word = {"word":word, "language_level":language_level}
                    writer.writerow(new_word)
                    nb_word += 1
                root.clear()

            elif tag == "title":
                word = value

                if is_exception(value):
                    WORD = False
                else:
                    WORD = True

            elif tag == "text":
                if is_french(value, word) and WORD == True:
                    k += 1
                    print("   ", word)
                    definitions = get_definition(value)

                    nb_def = len(definitions)
                    language_level = get_langage_level(definitions)
                    print(language_level)
                    print(value)
                    if language_level != "level1":
                        print(word)
                        print(language_level)
                else:
                    WORD = False

    fd.close()
    return nb_word


get_langage_level()

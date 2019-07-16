 # Welcome to the repository centralizing the lab's NLP resources.

Here is the list of the ressources and how they have been built:
 - *french.txt* is the french dictionary for linux systems;
 - *propernoun_exceptions.txt* is a list of nouns which are more often propre nouns. Thus a proper noun is a word which is capitalized and not in the french dictionary or either a word capitalized in this list;
 - *stopwords_ambigus.txt* is a list of stop words including ambiguous words, such as "est" or "bref";
 - *stopwords_français.txt* is a list of stop words without ambiguous words;
 - the folder **language_level** contains the *wiktionary.csv* which is a french dictionary with a language level tag for each word and the python script to build it. It needs also a dump of the definitions from the french wiktionary to be build.

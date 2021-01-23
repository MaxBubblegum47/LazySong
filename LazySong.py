import re
from nltk.stem import PorterStemmer
import math
import os
import pickle
import PySimpleGUI as sg
from typing import Dict
from autocorrect import Speller
from nltk.corpus import wordnet
import json

sg.ChangeLookAndFeel('Black')

class Gui:
    ''' Create a GUI object '''

    def __init__(self):
        sg.theme('Reddit')

        self.layout: list = [
            [sg.Text('Search', size=(11,1)),
             sg.Input(size=(40,1), focus=True, key="TERM"),
             sg.Checkbox('Synimous', size=(8, 1), default=False, key='syn_search')],
            [sg.Text('Data Path', size=(11,1)),
             sg.Input(None, size=(40,1), key="PATH"),
             sg.FolderBrowse('Browse', size=(10,1)),
             sg.Button('Build Index', size=(10,1), key="_INDEX_"),
             sg.Button('Search', size=(10,1), bind_return_key=True, key="_SEARCH_")],
            [sg.Output(size=(96,30))]]

        self.window: object = sg.Window('LazySong', self.layout, element_justification='left')

class QueryParsers:

    def __init__(self, file):
        self.filename = file
        self.query= self.get_queries()

    def get_queries(self):
        q = open(self.filename,'r', encoding = 'utf8').read().lower()
        #subsitute all non-word characters with whitespace
        pattern = re.compile('\W+')
        q = pattern.sub(' ', q)
        # split text into words (tokenized list for a document)
        q = q.split()
        # stemming words
        stemmer = PorterStemmer()
        q = [stemmer.stem(w) for w in q ]
        return q

class BuildIndex:

    b = 0.75
    k = 1.2

    def __init__(self, files):
        self.tf = {}
        self.df = {}
        self.filenames = files
        self.file_to_terms = self.process_files() #la lista delle liste dei termini di tutti i testi
        self.regdex = self.regular_index(self.file_to_terms)
        self.invertedIndex = self.inverted_index() #tutto l'inveted index
        self.dltable = self.docLtable()
        self.dl = self.docLen()
        self.avgdl = self.avgdocl()
        self.N = self.doc_n()
        self.idf = self.inverse_df()

    def process_files(self):
        '''
        input: filenames
        output: a dictionary keyed by filename, and with values of its term list
        '''
        file_to_terms = {}

        for file in self.filenames:
            #read the whole text of a file into a single string (if the text is not lowered add .lower() after .read())
            file_to_terms[file] = open(file,'r', encoding = 'utf-8', errors = 'ignore').read()
            #subsitute all non-word characters with whitespace
            pattern = re.compile('\W+')
            file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
            # split text into words (tokenized list for a document)
            file_to_terms[file] = file_to_terms[file].split()
            # if the text is not stemmed disable the after two comments stemming words
            #stemmer = PorterStemmer()
            #file_to_terms[file] = [stemmer.stem(w) for w in file_to_terms[file] ]
            #file_to_terms[file] = [w for w in file_to_terms[file] ]

        return file_to_terms

    def doc_n(self):
        '''
        return the number of docs in the collection
        '''
        return len(self.file_to_terms)


    def index_one_file(self, termlist):
        '''
        input: termlist of one document.
        map words to their position for one document
        output: a dictionary with word as key, position as value.
        '''
        fileIndex = {}
        for index,word in enumerate(termlist):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]

        return fileIndex

    def regular_index(self,termlists):
        '''
        input: output of process_files(filenames)
        output: a dictionary. key: filename, value: a dictionary with word as key, position as value
        '''
        regdex = {}

        for filename in termlists.keys():
            regdex[filename] = self.index_one_file(termlists[filename])

        return regdex


    def inverted_index(self):
        '''
        input： output of make_indexes function.
        output: dictionary. key: word, value: a dictionary keyed by filename with values of term position for that file.
        '''
        total_index = {}
        regdex = self.regdex

        for filename in regdex.keys():

            self.tf[filename] = {}

            for word in regdex[filename].keys():
                # tf dict key: filename, value: dict key is word, value is count
                self.tf[filename][word] = len(regdex[filename][word])

                if word in self.df.keys():
                    # df dict key: word, value: counts of doc containing that word
                    self.df[word] += 1
                else:
                    self.df[word] = 1

                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].extend(regdex[filename][word])
                    else:
                        total_index[word][filename] = regdex[filename][word]
                else:
                    total_index[word] = {filename: regdex[filename][word]}

        return total_index

    def docLtable(self):
        '''
        output: dict, key:word, value:dict(key: number of docs contaiing that word, value:total_freq)
        '''
        dltable = {}
        for w in self.invertedIndex.keys():
            total_freq = 0
            for file in self.invertedIndex[w].keys():
                total_freq += len(self.invertedIndex[w][file])

            dltable[w] = {len(self.invertedIndex[w].keys()):total_freq}

        return dltable

    def docLen(self):
        '''
        return a dict, key: filename, value: document length
        '''
        dl = {}
        for file in self.filenames:
            dl[file]=len(self.file_to_terms[file])
        return dl

    def avgdocl(self):
        sum = 0
        for file in self.dl.keys():
            sum += self.dl[file]
        avgdl = sum/len(self.dl.keys())
        return avgdl

    def inverse_df(self):
        '''
        output: inverse doc freq with key:word, value: idf
        '''
        idf = {}
        for w in self.df.keys():
            # idf[w] = math.log((self.N - self.df[w] + 0.5)/(self.df[w] + 0.5))
            idf[w] = math.log((self.N +1 )/self.df[w])
        return idf

class Ricerca:
    def __init__(self, s):
        q = QueryParsers("cronlogia.txt")
        query = q.get_queries()
        self.total_score  = Ricerca.BM25scores(s, query)
        self.rankedDocs = self.ranked_docs()

    def ranked_docs(self):
        ranked_docs = sorted(self.total_score.items(), key=lambda x: x[1], reverse=False)
        ranked_docs = list(filter(lambda x: x[1] != 0, ranked_docs))
        return ranked_docs

    def get_score (s,filename,qlist):
        '''
        filename: filename
        qlist: termlist of the query
        output: the score for one document
        '''
        score = 0
        for w in s.file_to_terms[filename]:
            if w not in qlist:
                continue
            wc = len(s.invertedIndex[w][filename])
            score += s.idf[w] * ((wc)* (s.k+1)) / (wc + s.k *
                                                                    (1 - s.b + s.b * s.dl[filename] / s.avgdl))
        return score

    def BM25scores(s,qlist):
        '''
        Output: a dictionary with filename as key, score as value
        '''
        total_score = {}
        for doc in s.file_to_terms.keys():
            total_score[doc] = Ricerca.get_score(s,doc,qlist)
        return total_score

def main():
    ''' The main loop for the program '''
    g = Gui()
    enable_search = False

    while True:
        event, values = g.window.read()

        #close windows
        if event is None:
           break

        if event == '_INDEX_' and values['PATH'] != '':
            #.DS_Store mess up everything if is there, so better remove it. Is produced by MacOS when you stuff like zip and
            #unzip folder, copy o move stuff from a place to another. It used by MacOS as a sort of summary of a particular
            #folder, but for our tasks is really terribile, because its encoding is not god for the program!
            bad_file = os.path.join(values['PATH'], '.DS_Store')
            if os.path.exists(bad_file):
                os.remove(bad_file)
            else:
                None

            print("Building the Inverted Index >>> ...")
            list_file=[]
            list_file = [(root, files) for root, dirs, files in os.walk(values['PATH']) if files]
            list_file.sort()
            lista_files = list()
            for path, files in list_file:
                #print(files) stampa di controllo per vedere se ispeziona tutti i file
                for canzoni in files:
                    lista_files.append((os.path.join(path,str(canzoni))))

            s = BuildIndex(lista_files)
            enable_search = True
            print("Done!\n")

        if event == '_SEARCH_' and enable_search == True and values['TERM'] != None:
            with open("cronlogia.txt", "w") as f:
                spell = Speller(lang='en')
                term_fix = spell(values['TERM'])
                term = values['TERM']
                print("Searching for >>> " + str(term))
                if term != term_fix:
                    print("Did you mean >>> " + term_fix)

                if values['syn_search'] == True:
                    syn = list()
                    for synset in wordnet.synsets(term):
                        for lemma in synset.lemmas():
                            if lemma.name() != term:
                                syn.append(lemma.name())
                    syn.insert(0, term)
                    print(syn)
                    #write every term in the cronologia.txt
                    for item in syn:
                        f.write("%s\n" % item)

                else:
                    f.write(term)

            search = Ricerca(s)
            result = search.rankedDocs
            numb = 1
            for elem in result:
                print("Result n.{} >>> ".format(numb)+ "Song: " + str(elem[0]) + " Score: " + str(elem[1]) + "\n")
                numb += 1
            f.close()

if __name__ == '__main__':
    print('Welcome Back!')
    main()
    print('Bye!')

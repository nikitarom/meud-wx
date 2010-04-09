import nltk
import math
import os
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from urllib import urlopen
from operator import itemgetter



def words_dist(root, Stemmer=1):
        """Function generates word frequences of the texts in a given directory."""
        wordlists = PlaintextCorpusReader(root, '.*')
        texts = []
        print 'Files in the directory: ', wordlists.fileids()
        texts = wordlists.fileids()
        stop = []
        freq = {}
        for text in texts:
                freq[text] = []
        for item in stopwords.words('english'):
                stop.append(str(item))
        for text in texts:
                words = wordlists.words(text)
                coll = []
                WORDS = []
                TEXT = []
                for w in words:
                        if (len(w) > 2 and w.isalpha() and w.lower() not in stop):
                                WORDS.append(w.lower())
                if Stemmer:
                        porter = nltk.PorterStemmer()
                        i = 0
                        while(i < len(WORDS)):
                                WORDS[i] = porter.stem(WORDS[i])
                                i += 1
                freq[text] = FreqDist(WORDS)
                TEXT = nltk.Text(WORDS)
                print text + ': ' 
                TEXT.collocations()
        return freq, texts


def tf(docfreq):
        count = 0
        termfreq = {}
        for word in docfreq:
                count += docfreq[word]
        for word in docfreq:
                termfreq[word] = docfreq[word] / float(count)
        return termfreq

def idf(word, texts, freq):
        numDocs = 0
        for text in freq:
                if word in freq[text]:
                        numDocs += 1
        return math.log(len(texts) / numDocs)

def dockeywords(docfreq, keywords):
        docwords = []
        for word in docfreq:
                if word in keywords:
                        docwords.append(word)
        return docwords
                        
        

def make_intent(freq):
        intent = []
        for text in freq:
                for word in freq[text]:
                        intent.append(word)
        return set(intent)


def main(root='C:/Users/Anastasia/HSE/PROJECT/texts'):
        freq, texts = words_dist(root)
        tf4word = {}
        tfidf = {}
        for text in freq:
                tf4word[text] = tf(freq[text])
        path4tf = str(root) + '/' + 'tf'
        savetf(tf4word, path4tf)
        
        idf4word = {}
        for word in list(make_intent(freq)):
                idf4word[word] = idf(word, texts, freq)

        for text in freq:
                tfidf[text] = {}
                for word in freq[text]:
                        tfidf[text][word] = tf4word[text][word] * idf4word[word]
        path4tfidf = str(root) + '/' + 'tfidf'
        savetfidf(tfidf, path4tfidf)

def savetf(tf4word, path2save='C:/Users/Anastasia/HSE/PROJECT/texts/tf'):
        for text in tf4word:
                textf = {}
                textf = tf4word[text]
                filename = str(path2save) + '/' + 'tf' + str(text)
                if not os.path.exists(path2save):
                        os.mkdir(path2save)
                f = open(filename, 'w')
                for item in sorted(textf.items(), key=itemgetter(1), reverse=True):
                        f.write( str(item[0]) + '\t' + str(item[1]) + '\n')
                f.close()
                

                

def savetfidf(tfidf, path2save='C:/Users/Anastasia/HSE/PROJECT/texts/tfidf'):
        for text in tfidf:
                textfidf = {}
                textfidf = tfidf[text]
                pathdir =  str(path2save) 
                filename = str(path2save) + '/' + 'tfidf' + str(text)
                if not os.path.exists(path2save):
                        os.mkdir(path2save)
                f = open(filename, 'w')
                for item in sorted(textfidf.items(), key=itemgetter(1), reverse=True):
                        f.write( str(item[0]) + '\t' + str(item[1]) + '\n')
                f.close()
                
                        

def create_context(cxtname, n, path='C:/Users/Anastasia/HSE/PROJECT/texts/tfidf'):
        os.chdir(path)
        files = os.listdir(path)
        texts = []
        textwords = {}
        for f in files:
                texts.append(f.split('.')[0][5:])
        for f in files:
                g = open(f, 'r')
                name = f.split('.')[0][5:]
                textwords[name] = []
                for line in g:
                        textwords[name].append(line.split()[0])
                g.close()
        docs2words = {}
        for text in textwords:
                wordlist = textwords[text]
                docs2words[text] = wordlist[:n]
        savecxt(cxtname, docs2words)
         

def read_keywords(filename, n):
        f = open(filename, "r")
        keywords = []
        for line in f:
                keywords.append(line.split()[0])
        return keywords[:n]

def paragraphs(par_root, keywordsfile, n, cxtpath):
        docwords = {}
        freq, texts = words_dist(par_root)
        keywords = read_keywords(keywordsfile, n)
        for text in freq:
                docwords[text] = dockeywords(freq[text], keywords)
        savecxt(cxtpath, docwords)
        
                
        
        
def savecxt(filename, users2tags):
        users = users2tags.keys()
        tags = [tag for tag in set(reduce(lambda x, y: x + y, users2tags.values()))]
        f = open(filename, "w")
        f.write("B\n\n" + str(len(users2tags)) + "\n" + str(len(tags)) + "\n\n")
        for u in users:
                f.write(str(u) + "\n")
        for t in tags:
                f.write(t + "\n")
        for u in users:
                row = ""
                for t in tags:
                        if t in users2tags[u]:
                                row += 'X'
                        else:
                                row += '.'
                f.write(row + "\n")
        f.close()



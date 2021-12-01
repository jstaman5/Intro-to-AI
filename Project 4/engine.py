from sklearn.feature_extraction.text import TfidfVectorizer
from crawler import *
from interface import *
import os
import pickle
import pandas as pd
import numpy as np

#SearchEngine

class SearchEngine:

    #constructor
    def __init__(self, mode, root = 'https://eecs.utk.edu/', depth = 1, verbose = 'F', query = ''):
        self.mode = mode
        self.verbose = verbose
        self.query = query
        self.root = root
        self.depth = depth

        #instantiate instances of crawler and interface
        self.interface = Interface(self.mode, self, self.query)
        self.crawler = WebCrawler(self.root, self.verbose)

        #call train
        self.train()
    
    def train(self):

        docs = os.path.exists('docs.pickle')
        links = os.path.exists('links.pickle')

        if(docs == True and links == True):
            #load both the cleaned documents and crawled links from their appropriate files
            file = open('docs.pickle', 'rb')
            file2 = open('links.pickle', 'rb')
            d = pickle.load(file)
            l = pickle.load(file2)
            self.crawler.set_documents(d)
            self.crawler.set_links(l)
            
        else:
            #delete file if there is only one
            if(docs == True):
                os.remove("docs.pickle")
            if(links == True):
                os.remove("links.pickle")
            #call the collect, crawl, and clean methods using the WebCrawler instance
            self.crawler.collect(self.root, self.depth)
            self.crawler.crawl()
            d = self.crawler.clean()
            l = self.crawler.get_links()
    
            with open('docs.pickle', 'wb') as f1:
                pickle.dump(d, f1)
            with open('links.pickle', 'wb') as f2:
                pickle.dump(l, f2)


        self.compute_tf_idf()

    #delete any .pickle files created
    def delete(self):

        docs = os.path.exists('docs.pickle')
        if(docs == True):
            os.remove("docs.pickle")
        
        links = os.path.exists('links.pickle')
        if(links == True):
            os.remove("links.pickle")


    def compute_tf_idf(self):
        
        #Instantiate the Tfidfvectorizer
        tfidf_vectorizer = TfidfVectorizer()

        #read in cleaned documents
        docs = self.crawler.get_documents()
        #print(len(docs))
       #print(docs)
        #Send our docs into the Vectorizer
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(docs)

        #Trasnpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()
        #print(X)
        #convert matrix into dataframe using feature names as dataframe index
        df = pd.DataFrame(X, index=tfidf_vectorizer.get_feature_names())

        return df, tfidf_vectorizer


    def handle_query(self):

        df, tfidf_vectorizer = self.compute_tf_idf()
        #print(df)
        #vectorize the query
        q = [self.query]
        
        q_vec = tfidf_vectorizer.transform(q).toarray().reshape(df.shape[0],)
        
        # Calculate cosine similarity.
        sim = {}
        #print(len(df.columns)-1)
        for i in range(len(df.columns)-1):
            if(np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec) != 0):
                sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
        
        #print(sim)
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        #print(sim_sorted)
        # Print the articles and their similarity values

        links = self.crawler.get_links()
        #print(docs[34])
        count = 0
        for k, v in sim_sorted:
            if v != 0.0 and k < len(links) and count < 5:
                count += 1
                print("["+str(k)+"] {} (".format(links[k]) + str("{:.2f}".format(v)) + ')')
        

    #call the listen() method of the SearchInterface
    def listen(self):
        self.interface.listen()

    #start function called in main.py
    def start(self):
        self.train()
        self.listen()
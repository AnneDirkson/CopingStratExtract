#!/usr/bin/env python
# coding: utf-8

# This script forms a module for the STR pipeline

# In[1]:


##load packages


import spacy
from negspacy.negation import Negex
from negspacy.termsets import termset
import pandas as pd
import pickle 
import re
import string


# In[2]:


###NOTE: in addition to packages, need to have spacy model ("en_core_web_sm") installed


# In[6]:


class NegationSTR(): 
    
    def __init__(self): 
        ts = termset("en")
        self.prec = ts.get_patterns()['preceding_negations']
        self.fol = ts.get_patterns()['following_negations']
        
        extra_fol = ['way back', 'as little as possible', 'worse']
        self.fol.extend(extra_fol)
        extra_prec = ['cut back', 'avoid', 'stay clear of', 'stay away from', 'limit', 'limited', 'stay out of', 'give up', 'gave up', 'free of', 'watch out', 'worse', 'minimize', 'no to', 'watch', 'watching']
        self.prec.extend(extra_prec)
        excluded = ['no', 'not']
        self.prec = [i for i in self.prec if i not in excluded]

    
    def load_obj(self,name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')
    

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    

    def check_against_negex (self, sent): 
        token_sent = sent.split(' ')
        spans_neg = [] 
#         prec2 = [' ' + i for i in self.prec]
        prec2 = self.prec
#         print(token_sent)

        for rule in prec2: 
            m = re.search(rule, sent)
            try: 

                c = 0
                y = []
                for num, l in enumerate(sent): 
    #                 print(num)
                    if m.start() <= num <= m.end(): 
                        y.append(c)
                    if l == ' ': 
                        c +=1
                y2 = list(set(y))

                top = 6 
                if len(token_sent) < y2[-1]+6: 
                    pass
                else:
                    for w in token_sent[y2[-1]:y2[-1]+6]: 
                        if w in string.punctuation: 
                            top +=1      
                nwtop = top
                for w in token_sent[y2[-1]+6:y2[-1]+nwtop]: 
                    if w in string.punctuation: 
                        top +=1        
                for z in range(1,top):
                    spans_neg.append(y2[-1]+z)
            except: 
                pass
#         print(self.fol)

        for rule in self.fol: 
            m = re.search(rule, sent)
            try: 
                c = 0
                y = []
                for num, l in enumerate(sent): 
                    if m.start() <= num <= m.end(): 
                        y.append(c)
                    if l == ' ': 
                        c +=1
                y2 = list(set(y))
                top = 6
                for z in range(1,top):
                    v = y2[0] -z
                    if v >= 0: 
                        w= token_sent[v]
                        if w in string.punctuation: 
                            top +=1 

                nwtop = top 
                for z in range(top,nwtop):
                    v = y2[0] -z
                    if v >= 0: 
                        w= token_sent[v]
                        if w in string.punctuation: 
                            top +=1      

                for z in range(1,top):
                    v = y2[0] -z
                    if v >= 0: 
                        spans_neg.append(v)

            except: 
                pass

        s = list(set(spans_neg))
        return s 


    def get_negation_dep (self, sent): 
#         nlp = spacy.load("en_core_web_sm")

        doc = self.nlp(sent)
        negated = []

        for token in doc:
            if token.dep_ == 'neg': 
                x = [token.head.text, token.head.i]
                negated.append(tuple(x))
            elif token.text == 'no' and token.dep_ == 'det': 
                x = [token.head.text, token.head.i]
                negated.append(tuple(x))
            elif token.text == 'non' and token.dep_ == 'amod': 
                x = [token.head.text, token.head.i]
                negated.append(tuple(x))
            else: 
                pass
        return negated
    

    
    def main_negation_func(self, ix, sent, ent_locs, tokenized = False): 
        
        
        if tokenized: 
#             tokenized_sent = sents
# #             tokenized_sent2 = [i.lower() for i in tokenized_sent]
            sent = " ".join(sent)
        
        sent = sent.lower()
        
#         print(sent)
            
        x1 = self.get_negation_dep (sent)
        x1_locs = [i[1] for i in x1]
        x1_txt = [i[0] for i in x1]
        x2 = self.check_against_negex(sent)
        negated = []
#         print(x1_locs)
#         print(x1_txt)
#         print(x2)

        for b in ent_locs: ##there will always just be one ent loc
            n = False

            if b in x2: 
                n = True
            if b in x1_locs: 
                for i in x1_locs: 
                    if b == i: 
                        n= True

            negated.append(n)
            
        return negated
        
    def main(self, inp):
        
        self.nlp = spacy.load("en_core_web_sm")
        
        negated = []
        cnt = 0
        for i,a,b in zip(inp.uniqix, inp.sent, inp.locs): 
            cnt +=1
            if cnt % 10000 ==0: 
                print(str(cnt) + ' of the ' + str(len(inp) + ' done'))
         
            if b == []: 
                negated.append([])
            else: 
                z = self.main_negation_func(i, a,b) 
                negated.append(z)

        df = pd.concat([inp, pd.Series(negated, name= 'negated')], axis=1)
        return df
    
    


# In[7]:


# ##EXAMPLE/ INPUT TYPE


# inp = NegationSTR().load_obj('./output_norm')

# ##NOTE: change input so that sentences are not tokenized.
# inp


# In[8]:


# inp.sent.iloc[0] ='The monkey in the bar took no beer'
# inp.sent.iloc[5] = 'Cut back on banana splits which are the best dessert'
# inp.locs.iloc[5] = [4,4,4,10, 4, 10,10]
# inp.sent.iloc[12] ='avoid the world tour'
# inp


# In[9]:


# inp.sent.iloc[11] ='avoid pretty flowers'
# # inp.sent.iloc[5] = 'Cut back on banana splits which are the best dessert'
# # inp.locs.iloc[5] = [4,4,4,10, 4, 10,10]
# inp


# In[11]:


# NegationSTR().main(inp)


# In[25]:


# def untokenize(row): 
#     tokenized_sent = row[0]
# #     tokenized_sent2 = [i.lower() for i in tokenized_sent]
#     sent = " ".join(tokenized_sent)
#     return sent

# inp.sent = inp.sent.apply(lambda x: untokenize(x))
# inp


# In[51]:


# NegationSTR().save_obj(inp, './example_negation_input')


# In[55]:


# t = [NegationSTR().main_negation_func(i, a,b,c) for i, a,b,c in zip(inp.sentix, inp.sent, inp.phrase, inp.locs)]

# df = pd.concat([inp, pd.Series(t, name= 'negated')], axis=1)
# df.head()

# # NegationSTR().save_obj(df, './output_negated')


# In[56]:


# NegationSTR().save_obj(df, './output_negated')


# In[ ]:





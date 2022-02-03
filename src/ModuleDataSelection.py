#!/usr/bin/env python
# coding: utf-8

# In[ ]:


###include sentence splitting annd Index creationg!


# In[35]:


##packages 

import re
from nltk.tokenize import word_tokenize
import pandas as pd 
from collections import defaultdict


# In[1]:


class DataSelection(): 
    
    def __init__(self): 
        pass
    
            
    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')
    

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    def select_ADR_zone(self,df): 
        filt = []
        yes_threads = defaultdict(list)
        for a,b,c in zip(df.threadix, df.docixs_num, df.adr_locs): 
            if c != []: 
                for y in range (b, b+5):
                    yes_threads[a].append(y)
                
                    
        for a,b in zip(df.threadix, df.docixs_num): 
            if a in yes_threads: 
                if b in  yes_threads[a]: 
                    filt.append(1)
                else: 
                    filt.append(0)
            else: 
                filt.append(0)
        
        df2 = pd.concat([df, pd.Series(filt, name= 'filt')],axis=1)
        
        nwdf = df2[df2.filt== 1]
        nwdf = nwdf.drop (columns ='filt')
        return nwdf
                
    
    def simple_sent_splitting (self,tokenizedsent, ix, ixnum, threadix, adrlocs, adrlbls): ##one sentence.
    
        nwsent = []
        nwixs = []
        tmp = []
        
        nwlbls = []
        tmplbls = []
        nwlblslocs = []
        tmplblslocs = []

        d_lbls = {}
        for a,b in zip(adrlbls, adrlocs): 
            d_lbls[b[0]] = a
        d_locs = {}
        for b in adrlocs: 
            d_locs[b[0]] = b

        for num,w in enumerate(tokenizedsent): 
            if num in d_locs: 
                tmplbls.append(d_lbls[num])
                tmplblslocs.append(d_locs[num])

            tmp.append(w)
            if w == '.' or w == '?' or w == '!': 
                try: 
                    if (re.fullmatch('\d+', tokenizedsent[num-1])) and re.fullmatch('\d+', tokenizedsent[num+1]): 
                        pass


                    else: 
                        nwsent.append(tmp)
                        nwlbls.append(tmplbls)
                        nwlblslocs.append(tmplblslocs)
                        tmp = []
                        tmplbls = []
                        tmplblslocs = []

                except IndexError: 
                    nwsent.append(tmp)
                    nwlbls.append(tmplbls)
                    nwlblslocs.append(tmplblslocs)
                    tmp = []
                    tmplbls = []  
                    tmplblslocs = []
            else: 
                pass

        if tokenizedsent[-1] != '.': 
            nwsent.append(tmp)
            nwlbls.append(tmplbls)
            nwlblslocs.append(tmplblslocs)
            tmp = []
            tmplbls = []  
            tmplblslocs = []

        nwixs = [ix] * len(nwsent) ##doc ixs
        nwixsnums = [ixnum] * len(nwsent) ##doc ixs
        
        nwthreadixs = [threadix] * len(nwsent) ##doc ixs

        sentixs = list(range(1,len(nwixs)+1))

        uniqixs = []
        for a,b in zip(sentixs, nwixs): 
            z = b + '-' + str(a)
            uniqixs.append(z)

        sents2 = [" ".join(i) for i in nwsent]

        return sents2, nwixs, sentixs, uniqixs, nwthreadixs, nwixsnums, nwlbls, nwlblslocs


    def run_sent_splitting(self,sents, ixs,threadixs, docnumixs, adrlbls, adrlocs):
        sents3 = []
        ixs3 = []
        sentixs3 = []
        uniq_ixs3 = []
        thread_ixs3 = []
        docnum_ixs3 = []
        lbls3 = []
        lblslocs3 =[]

        for a,b,c,d,e,f in zip(sents, ixs, threadixs, docnumixs, adrlbls, adrlocs): 
            sents2, ixs2, sentix2, uniqixs2, threadixs2, docnum_ixs2, lbls2, lblslocs2 = self.simple_sent_splitting(a,b, d,c,f,e)
            sents3.extend (sents2)
            ixs3.extend(ixs2)
            sentixs3.extend(sentix2)
            uniq_ixs3.extend(uniqixs2)
            thread_ixs3.extend(threadixs2)
            docnum_ixs3.extend(docnum_ixs2)
            lbls3.extend(lbls2)
            lblslocs3.extend(lblslocs2)

        df_split = pd.concat([pd.Series(ixs3, name = 'docix'),pd.Series(docnum_ixs3, name= 'docixs_num'),  pd.Series(sents3, name = 'sent'), 
                              pd.Series(sentixs3, name = 'sentix'), pd.Series(uniq_ixs3, name ='uniqix'), pd.Series(thread_ixs3, name= 'threadix'),
                             pd.Series(lbls3, name = 'adrlbl'), pd.Series(lblslocs3, name = 'adrlocs')], axis=1)
        return df_split

    
    def generate_numeric_doc_ixs (self, df): 
        
        curt = df.threadix.iloc[0]
        curd = df.docix.iloc[0]
        doc_ixs_num = []
        cnt = 1
        for a,b in zip(df.threadix, df.docix): 
            if curt != a: 
                cnt = 1
                curt = a
            elif curd != b: 
                cnt +=1 
                curd = b
            else: 
                pass
            doc_ixs_num.append(cnt)           
            
        nwdf = pd.concat([df, pd.Series(doc_ixs_num, name= 'docixs_num')], axis=1)
        
        return nwdf
    
        
    def main(self, df):
        df2 = self.generate_numeric_doc_ixs (df)
        df_select = self.select_ADR_zone(df2)
        df_split = self.run_sent_splitting(sents=df_select.sent, ixs=df_select.docix, threadixs = df_select.threadix, docnumixs = df_select.docixs_num, adrlbls = df_select.adr, adrlocs = df_select.adr_locs)
        
        df_split2 = df_split[df_split.sent != '']
        df_split2 = df_split2.reset_index(drop = True)
        
        return df_split2
    


# In[154]:


####still amend sentence splitting to figure out ADR locs 


# In[155]:


###NOTE the output is probably a tokenized sent! due to ADR tagging


# In[156]:


# ##fake data

# ##lets make fake dta 

# threadix = [1,1,1,1,1,2,2,2,2,2,2,2,3,3,3]
# threadixs2 = [str(i) for i in threadix]
# docix = [1,2,3,4,5,1,2,3,4,5,6,7,1,2,3]
# docixs2 = [str(i) for i in docix]
# # sentix = [1,2,3,4,5,1,2,3]
# # sentix2 =[str(i) for i in sentix]

# sents1 = ['The monkey in the bar took a beer. He laughed loud.', 'Mission impossible is what I heard', 'The train is leaving hte station. The carts may tip', 
#          'Banana splits are the best dessert', 'Comedy is an art form', 'The doctors thought the mysterious bulge was alien', 'The blue bus is faster than the yellow bus. Who would have thought?',
#         'Bees have knees', 'Flowers are pretty', 'Take the world lightly', 'Balloons fly into the sky', 'Red roses can also be blue', 'Pink is not only for princesses', 'Money cannot buy love', 
#         'Power moves']

# sents = [word_tokenize(i) for i in sents1]

# # locs = [[], [8], [10], [1], [2], [4],[],[]]

# adr_locs= [[[10], [11]], [[4,5], [10,11]], [], [[6,7]], [], [[1]], [[5,6]], [], [],[],[],[],[],[],[]]
# adrs = [[['heartache'], ['heartache']], [['foot issue'], ['hand issue']], [], [['nausea thing']], [], [['bruise']], [['toe pain']], [], [],[],[],[],[],[],[]]

# df = pd.concat([pd.Series(threadixs2, name ='threadix'), pd.Series(sents, name = 'sent'), pd.Series(docixs2, name = 'docix'), pd.Series(adr_locs, name= 'adr_locs'), pd.Series(adrs, name = 'adr')],axis=1)

# # df = load_obj('C:/Users/dirksonar/Documents/Data/Project13_LinkCoping/RelationData/OutputData_v3')


# In[157]:


# df


# In[158]:


# DataSelection().main(df)


# In[ ]:





# In[ ]:





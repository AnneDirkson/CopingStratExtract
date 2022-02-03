#!/usr/bin/env python
# coding: utf-8

# This is the RE module for ADR-coping

# In[1]:


###packages
import pandas as pd
import pickle 

# In[2]:


###NOTE I NEED THE DETAILS OF WHICH THREADS AND WHICH DOCUMENTS AND ADR TAGS 


# In[7]:


class RelationADR_STR(): 
    
    def __init__(self): 
        pass
    
        
    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')
    

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
            
    def select_ADR(self,df):
        out = []
        for a,b,c,d,e,f in zip(df.threadix, df.docix, df.sentix, df.locs, df.adrlbl, df.adrlocs): ##locs are relative to sentences (not to posts) - can be multiple 
            
            tmp = []
            for strat in d:
#                 print(strat)
                gotcha = 0
                dist = [strat-i[-1] for i in f] ##first looking for before 
#                 print(dist)
                try: 
                    j = dist.index(min([i for i in dist if i > 0]))
                    ##grab ADR 
#                     print(j)
                    correct_adr = e[j]
                    tmp.append(correct_adr)
                    gotcha = 1


                except ValueError: ##there are no ADR before in the sentence
#                     print('No ADR before')
                    ##check for ADR in earlier sentences of the post
                    df_thread = df[df.threadix == a]
                    nwdf = df_thread[df_thread.docix == b]
                    nwdf2 = nwdf[nwdf.sentix < c] ##exclude later sentences
                    ##compile
                    doc_adr = [i for j in list(nwdf2.adrlbl) for i in j]
#                             doc_adr_locs = [i for j in list(nwdf2.adr_locs) for i in j]
                    try: 
                        correct_adr = doc_adr[-1]
                        tmp.append(correct_adr)
                        gotcha = 1
                    except IndexError: ##there is no ADR in earlier sentences
                        ##time to check later in the post
                        dist = [strat-i[0] for i in f] 
                        try: 
                            j = dist.index(min([i for i in dist if i < 0]))
                            ##grab ADR 
                            correct_adr = e[j]
                            tmp.append(correct_adr)
                            gotcha = 1
                        except ValueError: ##no ADR later in sentence
                            nwdf2 = nwdf[nwdf.sentix > c] ## later sentences in post
                            doc_adr = [i for j in list(nwdf2.adrlbl) for i in j]
                            try: 
                                correct_adr = doc_adr[0] ##take the closest after
                                tmp.append(correct_adr)
                                gotcha = 1
                            except IndexError: ##there is no ADR in the post at all - need to look in the thread at earlier posts
                                nwdf_thread = df_thread[df_thread.docix < b] ##exclude later posts
                                ##compile
                                doc_adr = [i for j in list(nwdf_thread.adrlbl) for i in j]
                                try: 
                                    correct_adr = doc_adr[-1]
                                    tmp.append(correct_adr)
                                    gotcha = 1
                                except: 
                                    tmp.append('')
#                                     print('Not working')
                                        
            out.append(tmp)
            
            
        out_df = pd.concat([df, pd.Series(out, name= 'connected_adr')],axis=1)

        return out_df
                        
                            
            
            
            
            


# In[19]:


# RelationADR_STR().select_ADR(df)


# In[39]:


# dist = [-3, -4]
# j = dist.index(min([i for i in dist if i > 0]))


# In[40]:


###note still need to add a function that makes something numeric from the indexes that are probably strings.


# In[17]:


# ##load data 

# ##lets make fake dta 

# threadix = [1,1,1,1,1,2,2,2]
# threadixs2 = [str(i) for i in threadix]
# docix = [1,1,1,2,3,1,2,2]
# docixs2 = [str(i) for i in docix]
# sentix = [1,2,3,4,5,1,2,3]
# sentix2 =[str(i) for i in sentix]

# locs = [[], [8], [10], [],[2], [4],[],[]]

# adr_locs= [[[10]], [[4,5], [10,11]], [], [[6,7]], [], [], [[5,6]], []]
# adrs = [[['heartache']], [['foot issue'], ['hand issue']], [], [['nausea thing']], [], [], [['toe pain']], []]

# df = pd.concat([pd.Series(threadix, name ='threadix'), pd.Series(docix, name = 'docix'), pd.Series(sentix, name = 'sentix'), pd.Series(adr_locs, name= 'adrlocs'), pd.Series(adrs, name = 'adrlbl'), pd.Series(locs, name = 'locs')],axis=1)

# # df = load_obj('C:/Users/dirksonar/Documents/Data/Project13_LinkCoping/RelationData/OutputData_v3')


# In[ ]:


# ##load data 

# ##lets make fake dta 

# threadix = [1,1,1,1,1,2,2,2,2,2,2,2,3,3,3]
# threadixs2 = [str(i) for i in threadix]
# docix = [1,1,1,2,3,1,2,2]
# docixs2 = [str(i) for i in docix]
# sentix = [1,2,3,4,5,1,2,3]
# sentix2 =[str(i) for i in sentix]

# locs = [[], [8], [10], [1], [2], [4],[],[]]

# adr_locs= [[[10]], [[4,5], [10,11]], [], [[6,7]], [], [[1]], [[5,6]], []]
# adrs = [[['heartache']], [['foot issue'], ['hand issue']], [], [['nausea thing']], [], [['bruise']], [['toe pain']], []]

# df = pd.concat([pd.Series(threadix, name ='threadix'), pd.Series(docix, name = 'docix'), pd.Series(sentix, name = 'sentix'), pd.Series(adr_locs, name= 'adr_locs'), pd.Series(adrs, name = 'adr'), pd.Series(locs, name = 'locs')],axis=1)

# # df = load_obj('C:/Users/dirksonar/Documents/Data/Project13_LinkCoping/RelationData/OutputData_v3')


#!/usr/bin/env python
# coding: utf-8

# In[1]:


##packages

import pandas as pd
import pickle 
import numpy as np 
from collections import Counter


# In[13]:


class PostProcess(): 
    
    def __init__(self): 
        pass
        
    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')
    

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)    
            
            
    def remove_unconnected_and_empty(self, data): 
    #     data2 = data[data.lbl != []]

        filt= []
        for a, i in zip(data.lbl, data.connected_adr): 
            if a == []: 
                filt.append(1)
            else: 
                i2 = set(i)
                if list(i2) == ['']: 
                    filt.append(1)
                else: 
                    filt.append(0)
#         print(sum(filt))

        data = data.reset_index(drop = True)
        data3 = pd.concat([data, pd.Series(filt, name = 'filt')],axis=1)

        data4 = data3[data3.filt ==0]
        data4 = data4.drop (columns =['filt'])
        return data4

    def uncouple_sents_and_deduplicate (self,data): ##combine labels of same location -- I will assume the first label is the highest 
        nwsent = []
        nwuniqix = []
        nwlocs = []
        nwlblname = []
        nwlbl = []
        nwdocix = []
        nwthreadix= []
        nwnegated = []
        nwconnected = []
        nwadrlocs = []
        cnt = 0


        for a,b,c,d,e,f,g,h,i,j in zip(data.sent, data.uniqix, data.locs, data.lblname, data.lbl, data.docix, data.threadix, data.negated, data.connected_adr, data.adrlocs): 
            locs_done = []
            for c1,d1,e1, h1, i1 in zip(c,d,e,h,i):

                if c1 in locs_done:
                    cnt +=1 ## we have already had this location
                    pass


                else: 

                    nwsent.append(a)
                    nwuniqix.append(b)
                    nwlocs.append(c1)
                    nwlbl.append(e1)
                    nwlblname.append(d1)
                    nwdocix.append(f)
                    nwthreadix.append(g)
                    nwnegated.append(h1)
                    nwadrlocs.append([k for m in j for k in m])
                    nwconnected.append(i1)

                    locs_done.append(c1)



        df = pd.concat([pd.Series(nwsent, name = 'sent'), pd.Series(nwuniqix, name = 'uniqix'), pd.Series(nwlocs, name= 'locs'), pd.Series(nwlbl, name= 'lbl'), pd.Series(nwlblname, name = 'lblname'), pd.Series(nwdocix, name= 'docix'),pd.Series(nwthreadix, name= 'threadix'), pd.Series(nwnegated, name= 'negated'), pd.Series(nwconnected, name= 'connected_adr'), pd.Series(nwadrlocs, name = 'adr_locs')], axis=1)
        return df
            
    def remove_if_ADR_location(self,data): 
        filt = []

        for a,b in zip(data.locs, data.adr_locs): 
            if a in b: 
                filt.append(1)
            else: 
                filt.append(0)
#         print(sum(filt))

        data = data.reset_index(drop = True)
        nwdata = pd.concat([data, pd.Series(filt, name = 'filt')], axis =1)

        nwerdata = nwdata[nwdata.filt ==0]
        nwerdata = nwerdata.drop (columns = ['filt'])
        return nwerdata
    
    def uniqix_combinatorial (self,data): 
        entix= []
        cnt = 1
        combo = False
        prevuniqix = ''
        for num, a in enumerate(data.locs): 
            if combo == True: 
                entix.append(nwix)
                combo = False
            else:
                d = data.uniqix.iloc[num]

                if d != prevuniqix: 
                    cnt = 1
                    prevuniqix = d

                nwix = d + '-' + str(cnt)


                if num != len(data)-1:
                    b = data.negated.iloc[num]
                    c = data.connected_adr.iloc[num]

                    d2 = data.uniqix.iloc[num+1]
                    if d == d2:

                        nxtloc= data.locs.iloc[num+1]
                        nxtadr = data.connected_adr.iloc[num+1]
                        nxtcon = data.negated.iloc[num+1]

                        if nxtloc - a ==1: 
                            if (nxtadr == c) & (nxtcon == b): 
        #                         print('There is a case')
        #                         print(num)
                                nwix = d + '-' + str(cnt)
                                combo = True

                cnt += 1
                entix.append(nwix)


        return entix
    
    def change_to_one(self,row): 
        return row [0]
    
    def make_startletter_df(self, data): 
        c = Counter(data.connected_adr)

        v = c.most_common(200)

        names = [i[0] for i in v]
        rank = [i for i in range(1, 201)]
        rank2 = [str(i) for i in rank]

        startltr = [i[0] for i in names]

        df = pd.concat([pd.Series(names, name= 'ADE'), pd.Series(rank2, name= 'Rank'), pd.Series(startltr, name= 'ltr')], axis=1)

        return df

        
    def main(self,data): 
        nwdata = self.remove_unconnected_and_empty(data)
        nwerdata = self.uncouple_sents_and_deduplicate (nwdata)
        
        nwerdata0 = self.remove_if_ADR_location(nwerdata)
        nwerdata1 = nwerdata0.sort_values(by=['uniqix', 'locs'], ascending = [True, True])
        entix = self.uniqix_combinatorial (nwerdata1)
        nwerdata1 = nwerdata1.reset_index(drop = True)
        nwerdata2 = pd.concat([nwerdata1, pd.Series(entix, name= 'entix')],axis=1)
        aggdata = nwerdata2.groupby('entix').agg(list)

        ##change to one 
        
        aggdata.docix = aggdata.docix.apply(lambda x: self.change_to_one(x))
        aggdata.uniqix = aggdata.uniqix.apply(lambda x: self.change_to_one(x))
        aggdata.sent = aggdata.sent.apply(lambda x: self.change_to_one(x))
        
        aggdata.threadix = aggdata.threadix.apply(lambda x: self.change_to_one(x))
        
        aggdata.connected_adr = aggdata.connected_adr.apply(lambda x: self.change_to_one(x))
        aggdata.negated = aggdata.negated.apply(lambda x: self.change_to_one(x))
        aggdata.adr_locs = aggdata.adr_locs.apply(lambda x: self.change_to_one(x))
        
        
        df_startltr = self.make_startletter_df(aggdata)
        
        return aggdata, df_startltr


# In[14]:



# data = PostProcess().load_obj('C:/Users/dirksonar/Documents/Data/Project13_LinkCoping/Fullrun/Fullrun_Coping_output_data')


# In[15]:


# data2 = PostProcess().main(data)


# In[16]:


# data2.head()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##this will also include the MVP assessment. 


# In[1]:


##load packages 
import pandas as pd
import pickle 
import numpy as np

from sentence_transformers import SentenceTransformer, util
import torch


# In[69]:


class STRNormalization(): 
    
    def __init__(self): 
        pass
    
    
    def create_lbl_embeddings(self, lbls): ##lblset has lable names, not numbers 

        model = SentenceTransformer('all-MiniLM-L6-v2')
        ##Make document embeddings once 
        lbl_embed = model.encode(lbls)
        return lbl_embed

    
    def MultiLabel(self, dictpath, data): ##main function
    
        dict_names = self.load_obj(dictpath)
        
        lbls = [v for k,v in dict_names.items()]
        keys = [k for k,v in dict_names.items()]
        lbl_embed = self.create_lbl_embeddings(lbls)
        
        docs = data.sent
        output_semsim = self.query_semsim_model(docs, lbls, lbl_embed)
        
        output_semsim_lbls, output_semsim_keys = self.thresholding(output_semsim, lbls, keys)
#         print(output_semsim_lbls)
#         print(output_semsim_keys)
        locs_mvp_words = self.retrieve_approx_locations(docs, output_semsim_lbls)
        
        ##make a df and save 
        
        df = pd.concat([data, pd.Series(locs_mvp_words, name= 'locs'), pd.Series(output_semsim_lbls, name ='lblname'),pd.Series(output_semsim_keys, name ='lbl')], axis=1)
        
        return df
        ##ADD SAVE LATER 
      
        
    def thresholding(self,data, lbls, keys, thres = 0.5): 
        nwdata_lbls = []
        nwdata_keys = []
        for i in data: 
            lbls_doc = [j[0] for j in i if j[1] >= thres ]
            lbls_doc2 = [lbls[num] for num in lbls_doc]
            keys_docs = [keys[num] for num in lbls_doc]
            
            #
            nwdata_lbls.append(lbls_doc2)
            nwdata_keys.append(keys_docs)
            
        return nwdata_lbls, nwdata_keys     
        

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')


    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
            
    def retrieve_approx_locations(self,docs, output, mvp = True): 
        tok_docs = [i.split(' ') for i in docs]
     
        ##output should be list of lbls for each document
        
        nwoutput= []
        for tok,lbl_lst in zip(tok_docs, output): 
            tmp_out = []
            for l in lbl_lst: 
                l2 = [l]
                lbl_embed_tmp = self.create_lbl_embeddings(l2)
                tmp = self.query_semsim_model(tok, l2, lbl_embed_tmp, mvp)
#                 print(tmp)
                tmp2 = tmp.index(max(tmp))    
                tmp_out.append(tmp2)
            nwoutput.append(tmp_out)
        return nwoutput

    def query_semsim_model (self, queries, lbls, lbl_embed, mvp = False):

        output= []
        model = SentenceTransformer('all-MiniLM-L6-v2')

        ##can cap at 100 here because it is document based 
        if mvp: 
            top_k = 1
        else:
            top_k = 100 ##
        cnt = 0
        for query in queries:

            query_embedding = model.encode(query, convert_to_tensor=True)

            cos_scores = util.pytorch_cos_sim(query_embedding, lbl_embed)[0]

            top_results = torch.topk(cos_scores, k=top_k)

            c = top_results
            temp = []
            for score, idx in zip(c[0], c[1]):
                temp.append(tuple([np.int(idx), np.float(score)]))
            output.append(temp)    
        return output



        
    


# In[34]:


# ##make fake data 
# docs = ['The monkey ate the banana on a chair', 'The person had a great time at the zoo and took some prednisol']

# ixs= ['docs1', 'docs2']

# df = pd.concat([pd.Series(docs, name= 'sent'), pd.Series(ixs,name = 'ix')], axis=1)
# df.head()


# In[35]:


# STRNormalization().save_obj(df, './fake_data_semsim')


# In[70]:


# dictpath = 'C:\\Users\\dirksonar\\Documents\\Data\\Project13_LinkCoping\\Ontology_Sub/dictionary_CSix_names_new'
# datapath =  './fake_data_semsim'
# # datapath = 

# out_df = STRNormalization().MultiLabel(dictpath, datapath)


# In[71]:


# out_df.head()


# In[52]:


# output= out_df.lbl
# docs = out_df.sent 


# dict_names = STRNormalization().load_obj(dictpath)
        
# lbls = [v for k,v in dict_names.items()]
# # lbl_embed = STRNormalization().create_lbl_embeddings(lbls)

# # STRNormalization().retrieve_approx_locations(self,docs, output, lbl_embed)


# In[53]:


# for l in output: 
#     print(l)


# In[67]:



# STRNormalization().retrieve_approx_locations(docs, output, mvp= True)


# In[ ]:





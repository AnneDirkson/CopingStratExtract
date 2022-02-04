#!/usr/bin/env python
# coding: utf-8

# In[3]:


##import modules 

from ModuleDataSelection import DataSelection
from ModuleMultilabel import STRNormalization

from RelationExtractionModule import RelationADR_STR
from NegationSTRModule import NegationSTR
from ModulePostProcess import PostProcess


# In[4]:


import pandas as pd
import pickle


# In[6]:


class STRExtraction(): 
    
    def __init__(self): 
        pass
    
    def load_obj(self,name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')
    

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    def main(self,datapath,outpath): 
        
        data = self.load_obj(datapath)
#         print(data.head())
        sel_data = DataSelection().main(data)
        self.save_obj(sel_data, outpath+ '/selected_data_norm')
        print('Data selection done')
       
        norm_data = STRNormalization().MultiLabel('./dictionary_CSix_names_new', sel_data)
        self.save_obj(norm_data, outpath +'/output_norm')
        print('Normalization done')
    
        norm_data_wneg = NegationSTR().main(norm_data)
        self.save_obj(norm_data_wneg, outpath + "/negated_data")
        print('Negation done')
      
        norm_data_wneg_wrel = RelationADR_STR().select_ADR(norm_data_wneg)
        
        self.save_obj(norm_data_wneg_wrel, outpath + "/negated_data_wrel")
        
        output_data, df_startltr = PostProcess().main(norm_data_wneg_wrel)
        self.save_obj(output_data, outpath + "/Fullrun_Coping_output_data")
        
        self.save_obj(df_startltr, outpath + '/df_start_ltr')
        return output_data


# In[ ]:


STRExtraction().main('./example-data', './Output')


# In[7]:


# STRExtraction().load_obj('./fake-start-data')


# In[ ]:





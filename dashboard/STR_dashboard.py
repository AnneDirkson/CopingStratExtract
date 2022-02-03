#!/usr/bin/env python
# coding: utf-8

# This is the script for the interactive real dashboard for exploring the CS data 

# In[64]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pickle 

import plotly.express as plt 
import plotly.graph_objects as go

from collections import Counter

import dash_table


# In[66]:




# In[67]:

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f, encoding='latin1')

# data = load_obj('C:/Users/dirksonar/Documents/Data/Project13_LinkCoping/Fullrun/Fullrun_Coping_output_data_clean_viz')

# df_ltr = load_obj('startletter_df')
    
data = load_obj('./Output/Fullrun_Coping_output_data"')

df_ltr = load_obj('./Output/df_start_ltr')
    

# In[70]:


# make_graph_certain_ADE('Nausea', data, 20)


# In[71]:


import pandas as pd





# In[72]:


# print_cs_ade('Ondansetron', 'Nausea', data)


# In[73]:


# app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    

app.layout = html.Div([
    html.H1('Dashboard for viewing coping strategies'),
    
    html.Div([
        html.Div("If you want to find a specific side effect, fill in the first letter here to find its ranking (top 200 included only):"), 
        dcc.Input (type= 'text', id ='alpha-input', value = 'A', placeholder = 'A'),
        
        dcc.Graph(id='rankings'), 
    ]),
    
    
    
    html.Div("You see the graph with Coping Strategies per side effect. How far down the list do you want to see? (Default is 10)"),
    dcc.Input(id="topnum", type="number", max = 200, min = 10, value=10),
    
    html.Div(dcc.Graph(id='graph_topade'),),
    
    html.Div(
        [html.Div("If you want to take a closer look at one of these side effects, fill it in here: (Default is the 1st)"), 
         dcc.RadioItems(id='dropdown1'),
         html.Div(id='display-selected-values'),
        ],
    ),
    
    html.Div("\n How far down the list do you want to see? (Default is 10)"),
    dcc.Input(id="topnum2", type="number", max = 100, min = 10, value=10),
    
    html.Div(dcc.Graph(id = 'graph_topCS'),),
    
       
    html.Div(
        [html.Div("If you want to take a closer look at the messages about one of these coping strategies, fill it in here: (Default is the 1st)"), 
         dcc.RadioItems(id='dropdown2'),
         html.Div(id='display-selected-values2'),
        ],
    ),
    
    html.Div(
        [
        dcc.Graph(
        id='msgsCS'),
        ],
        ), 
#     html.Div(id = 'msgsCS', style={"maxHeight": "400px", "overflow": "scroll"}),
])


@app.callback(
    Output('rankings', 'figure'), 
    [Input ('alpha-input', 'value')],)
def alphabetical(ltr): 
    ltr = ltr.upper()
    d = df_ltr[df_ltr.ltr == ltr]
    
    fig = go.Figure(data=[go.Table(
        header = dict(values = ["ADE","Rank"]),
        cells=dict(values=[d.ADE, d.Rank], align='left')),
        ])
    
    fig.update_layout(width=600) 
    
    return fig

@app.callback(
    Output("graph_topade", "figure"),
    [Input('topnum', 'value')],
)
def graph_topADE (top=10): 
    
    c = Counter(data.connected_adr)
    
    v = c.most_common(top)
    
    t = top-10
    x0 = [i[0] for i in v]
    y0 = [i[1] for i in v]
    
    x = x0[t:top]
    y = y0[t:top]

    fig = plt.bar(y =x, x=y, orientation = 'h', text_auto=True,  width=600, height=400)
    
    ttl = "Top " + str(t+1) + ' - ' + str(top)

    fig.update_layout(yaxis=dict(autorange="reversed"), 
                     xaxis_title="Number of Coping Strategies", yaxis_title="Adverse Drug Event", title = ttl)

    fig.update_traces(marker_color='darkgreen')
#     fig.write_image('C:\\Users\\dirksonar\\Documents\\Analysis\\Project13_LinkCoping\\Graphs/top10ADE.pdf')
    return fig

# In[75]:

@app.callback(
    [Output("dropdown1", 'options'),
    Output('dropdown1', 'value')],
    [Input('topnum', 'value')],
)
def get_topADE (top=10): 
    
    c = Counter(data.connected_adr)
    
    v = c.most_common(top)
    
    t = top-10
    x0 = [i[0] for i in v]
    y0 = [i[1] for i in v]
    
    x = x0[t:top]

#     fig.write_image('C:\\Users\\dirksonar\\Documents\\Analysis\\Project13_LinkCoping\\Graphs/top10ADE.pdf')
    return [{'label': i, 'value': i} for i in x],  x[0]


@app.callback(
    Output("graph_topCS", 'figure'),
    [Input('dropdown1', 'value'), 
     Input('topnum2', 'value')],
)
def make_graph_certain_ADE(ade, top=10): 
    v = data[data.connected_adr == ade]
    
    flat0 = [i for j in v.lblname for i in j]
    
    flat = [i.capitalize() for i in flat0]
    c = Counter(flat)

    v = c.most_common(top)
    
    t = top-10
    x0 = [i[0] for i in v]
    y0 = [i[1] for i in v]
    
    y = x0[t:top]
    x = y0[t:top]


    fig = plt.bar(x = x, y= y, orientation = 'h',  text_auto=True,  width=700, height=420)
    fig.update_traces(marker_color='darkgreen')

    
       
    ttl = "Top " + str(t+1) + ' - ' + str(top) + " for " + str(ade)
    fig.update_layout(yaxis=dict(autorange="reversed"), 
                     xaxis_title="Frequency", yaxis_title="Coping Strategy", title = ttl)

#     fig.update_traces(marker_color='darkgreen')
    return fig


@app.callback(
    [Output("dropdown2", 'options'),
    Output('dropdown2', 'value')],
    [Input('dropdown1', 'value'),
    Input('topnum2', 'value')],
)
def get_optionsCS (ade, top): 
    
    v = data[data.connected_adr == ade]
    
    flat0 = [i for j in v.lblname for i in j]
    
    flat = [i.capitalize() for i in flat0]
    c = Counter(flat)

    v = c.most_common(top)
    
    t = top-10
    x0 = [i[0] for i in v]
    y0 = [i[1] for i in v]
    
    x = x0[t:top]
#     x = y0[t:top]

#     fig.write_image('C:\\Users\\dirksonar\\Documents\\Analysis\\Project13_LinkCoping\\Graphs/top10ADE.pdf')
    return [{'label': i, 'value': i} for i in x],  x[0]




@app.callback(
    Output("msgsCS", 'figure'),
    [Input('dropdown2', 'value'), 
     Input('dropdown1', 'value')],
)
def print_cs_ade(cs,ade): 
    v = data[data.connected_adr == ade]
    cs2 = cs.lower()
    filt = []
    for i in v.lblname: 
        q = 0
        for z in i: 
            if z == cs2:
                
                q =1 
                
        filt.append(q)
    
    v = v.reset_index()
    df = pd.concat([v, pd.Series(filt, name= 'filt')], axis=1)
    df2 = df[df.filt==1]
    
    lst_msg = list(df2.docix)

    nwdata = data[data.docix.isin(lst_msg)]
    
    nwdata2 = pd.concat([nwdata.sent, nwdata.docix],axis=1)
    nwdata2 = nwdata2.drop_duplicates()
    
    aggdata = nwdata2.groupby('docix').agg(list)
    
    x = list(aggdata.sent)
    
    x0 = [' '.join(i) for i in x]
    
    p = pd.Series(x0)
#     x1 = [i + ' &nbsp ' for i in x0]
#     for i in x0: 
#         print(i)
#         print('\n')

    fig = go.Figure(data=[go.Table(
            cells=dict(values=[p],
                       fill_color='lavender',
                       align='left'))
        ])

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





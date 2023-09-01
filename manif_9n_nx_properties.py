import numpy as np 
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from decimal import Decimal
from datetime import date, datetime, timedelta
from pandas.plotting import register_matplotlib_converters
import sys
import matplotlib.dates as mdates
import community
from networkx.algorithms import approximation
#from nestedness_calculator import NestednessCalculator

caso="9n"
print caso
#print ("\n")
register_matplotlib_converters()

edge = pd.read_csv('D:/Documentos/Master_BigData/14-TFM/VisualStudio/csv/weighted_Edge_list_9n.csv')
data = pd.read_csv('D:/Documentos/Master_BigData/14-TFM/VisualStudio/csv/Data_9n.csv')
data['inhashtag'] = data['hashtag'].astype(int)

#print(data['inhashtag'])

edge["hour"] = 3600 * edge["hour"]
data["hour"] = 3600 * data["hour"]
#print(edge)

edge["human_hour"] = pd.to_datetime(edge["hour"],unit='s')
data["human_hour"] = pd.to_datetime(data["hour"],unit='s')
#print(edge)

#ini = edge["hour"].min()
#fin = edge["hour"].max()

if caso == '15m':                                    # change the date here
    ini = datetime(2011, 05, 14, 06, 00)
    fin = datetime(2011, 05, 16, 23, 00)
    y0 = 1750
    y1 = 12
    x1 = datetime(2011, 5, 15, 23, 0)
    xc = datetime(2011, 05, 15, 12, 0)

elif caso == 'noaltarifazo':    
    ini = datetime(2019, 01, 01, 06, 00)
    fin = datetime(2019, 01, 07, 23, 00)
    y0 = 1450
    y1 = 7.2
    x1 = datetime(2019, 1, 5, 0, 0)
    xc = datetime(2019, 1, 4, 3, 0)
    
elif caso == '9n':    
    ini = datetime(2019, 11, 10, 14, 00)
    fin = datetime(2019, 11, 10, 15, 00)
#    fin = datetime(2019, 11, 8, 06, 01)
    y0 = 1500
    y1 = 7.7
    x1 = datetime(2019, 11, 9, 21, 0)
    x2 = datetime(2019, 11, 10, 21, 0)
    xc = datetime(2019, 11, 9, 3, 0)   
    
def datespan(startDate, endDate, delta=timedelta(hours=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

#fig, axs = plt.subplots(2)
for timestamp in datespan(ini,fin,delta=timedelta(hours=1)):
   average = 0
   average2 = 0
   print (timestamp)
   short_edge = edge[edge['human_hour'] == timestamp] [['h1','h2','hour','weight']]
   short_data = data[data['human_hour'] == timestamp] [['user','hashtag','inhashtag','hour']] 
   short_edge = short_edge.reset_index(drop=True)
   short_data = short_data.reset_index(drop=True)
   nusers = short_data['user'].nunique()
   
#   print(short_data)
#   print(short_edge)
   G=nx.from_pandas_edgelist(short_edge,'h1','h2',edge_attr='weight')
   pr=nx.pagerank(G,0.85)
   ev_centrality = nx.eigenvector_centrality(G)
   centrality = nx.degree_centrality(G)
   closeness_centrality = nx.closeness_centrality(G)
   betweenness_centrality = nx.betweenness_centrality(G)
   clustering_value = approximation.average_clustering(G, trials=1000, seed=10)
   Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
   G0 = G.subgraph(Gcc[0])
   path_length = nx.average_shortest_path_length(G0)
   print('Clustering value: ' +str(round(clustering_value,4)))
   print('Path length: ' + str(round(path_length,4)))

   #core_periphery = nx.periphery(G0) 
   #print(pr)
   #print('Periphery: ' + str(core_periphery))
   #print(ev_centrality)
   
   pr = pd.DataFrame.from_dict(pr, orient='index' , columns= ['Value'])
   print('PageRank mean: ' + str(round(pr.Value.mean(),4)))
   pr['Value'].plot(kind='hist')
   #pr_plot = pr.hist(column='Value')
   plt.title("PageRank Distribution")
   plt.xlabel("Value")
   plt.ylabel("Count")
   plt.show()

   
   ev_centrality = pd.DataFrame.from_dict(ev_centrality, orient='index' , columns= ['Value'])
   print('Eigenvector centrality mean: ' + str(round(ev_centrality.Value.mean(),4)))
   ev_centrality['Value'].plot(kind='hist')
   #ev_centrality_plot = ev_centrality.hist(column='Value')
   plt.title("Eigenvector Centrality Distribution")
   plt.xlabel("Value")
   plt.ylabel("Count")
   plt.show()

   centrality = pd.DataFrame.from_dict(centrality, orient='index' , columns= ['Value'])
   print('Centrality mean: ' + str(round(centrality.Value.mean(),4)))
   centrality['Value'].plot(kind='hist')
   #centrality_plot = centrality.hist(column='Value')
   plt.title("Centrality Distribution")
   plt.xlabel("Value")
   plt.ylabel("Count")
   plt.show()

   closeness_centrality = pd.DataFrame.from_dict(closeness_centrality, orient='index' , columns= ['Value'])
   print('Closeness centrality mean: ' + str(round(closeness_centrality.Value.mean(),4)))
   #closeness_centrality['Value'].plot(kind='hist')
   closeness_centrality_plot = closeness_centrality.hist(column='Value')
   plt.title("Closeness_centrality Distribution")
   plt.xlabel("Value")
   plt.ylabel("Count")
   plt.show()

   betweenness_centrality = pd.DataFrame.from_dict(betweenness_centrality, orient='index' , columns= ['Value'])
   print('betweenness_centrality mean: ' + str(round(betweenness_centrality.Value.mean(),4)))
   #betweenness_centrality['Value'].plot(kind='hist')
   betweenness_centrality = betweenness_centrality.hist(column='Value')
   plt.title("betweenness_centrality Distribution")
   plt.xlabel("Value")
   plt.ylabel("Count")
   plt.show()

   n = nx.number_connected_components(G)
   #print n
   GG = nx.to_numpy_array(G,weight=None)
#   nest = NestednessCalculator(GG).nodf(GG)
#   print('En',timestamp,'hay',G.number_of_nodes(),'nodos',',',G.number_of_edges(),'enlaces y',n,'componentes')
   ncompo=0
   if n>0 :
     part = community.best_partition(G,weight='weight')
     r=community.modularity(part,G)
   if r > 0.60: 
      #axs[0].scatter(timestamp,nusers,s=10,c='black')
      #axs[1].scatter(timestamp,r,s=10,c='blueviolet')
#     axs[1].scatter(timestamp,nest,s=10,c='red')  
     #print(r)
     for component in nx.connected_component_subgraphs(G):
         users = []
         nn = component.number_of_nodes()
         path = nx.average_shortest_path_length(component) 
         average += nn
         ncompo+=1
#         print ("En componente numero",ncompo,'hay',component.number_of_nodes(),'nodos',)
         lista = component.nodes()
         #print(lista)
         usuarios = []
         for has in lista:
#           print int(has)
#           print (short_data.loc[short_data["inhashtag"] == int(has)] ) 
           finding = short_data['user'].loc[short_data["inhashtag"] == int(has)]
           for cada in finding:
              if cada not in usuarios:
                 usuarios.append(cada)
#           print (len(usuarios),'usuarios en elhashtag',int(has),'del componente numero',ncompo)
         for ca in usuarios:
            if ca not in users:
              users.append(ca)
#         print users     
         nu = len(users)
         #axs[0].scatter(timestamp,nu,s=10,c='r')
#         axs[1].scatter(timestamp,path,s=10,c='b')
         average2 += nu
     average2 = average2 / n   
#     axs[0].scatter(timestamp,average2,s=10,c='magenta')      
     average = average / n
     #print timestamp
     #print ("\n")
#     axs[1].scatter(timestamp,average,s=10,c='b')
#     plt.title("In blue Average number of users in components, in red scatter number of users in components")
       

import numpy as np 
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import networkx as nx
from datetime import date, datetime, timedelta
from pandas.plotting import register_matplotlib_converters
import sys
import matplotlib.dates as mdates
import community
#from nestedness_calculator import NestednessCalculator

caso="noaltarifazo"
print (caso)
print ("\n")
register_matplotlib_converters()

edge = pd.read_csv("csv/weighted_Edge_list_noaltarifazo.csv")
data = pd.read_csv("csv/Data_noaltarifazo.csv")
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
    ini = datetime(2011, 5, 14, 6, 00)
    fin = datetime(2011, 5, 16, 23, 00)
    y0 = 1750
    y1 = 12
    x1 = datetime(2011, 5, 15, 23, 0)
    xc = datetime(2011, 5, 15, 12, 0)

elif caso == 'noaltarifazo':    
    ini = datetime(2019, 1, 7, 6, 00)
    fin = datetime(2019, 1, 7, 23, 00)
    y0 = 1450
    y1 = 7.2
    x1 = datetime(2019, 1, 5, 0, 0)
    xc = datetime(2019, 1, 4, 3, 0)
    
elif caso == '9n':    
    ini = datetime(2019, 11, 10, 10, 00)
    fin = datetime(2019, 11, 10, 20, 00)
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
listaTotal = list()
cont = 0
for timestamp in datespan(ini,fin,delta=timedelta(hours=1)):
   BigList = list()
   average = 0
   average2 = 0
#   print timestamp
   short_edge = edge[edge['human_hour'] == timestamp] [['h1','h2','hour','weight']]
   short_data = data[data['human_hour'] == timestamp] [['user','hashtag','inhashtag','hour']] 
   short_edge = short_edge.reset_index(drop=True)
   short_data = short_data.reset_index(drop=True)
   nusers = short_data['user'].nunique()
   
#   print(short_data)
#   print(short_edge)
   G=nx.from_pandas_edgelist(short_edge,'h1','h2',edge_attr='weight')
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
     cont += 1
     for component in nx.connected_component_subgraphs(G):
         users = []
         nn = component.number_of_nodes()
         path = nx.average_shortest_path_length(component) 
         average += nn
         ncompo+=1
#         print ("En componente numero",ncompo,'hay',component.number_of_nodes(),'nodos',)
         lista = component.nodes()  
         listaV2 = list(lista)
         if len(listaV2)>len(BigList):           
            BigList = listaV2      
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

     listaTotal.append(BigList)
     #print timestamp
     #print ("\n")
#     axs[1].scatter(timestamp,average,s=10,c='b')
#     plt.title("In blue Average number of users in components, in red scatter number of users in components")



# Find the number of common elements in both lists
common_elements = set(listaTotal[0]).intersection(*listaTotal[1:])
num_common_elements = len(common_elements)

# Find the total number of unique elements in both lists
total_elements = set(listaTotal[0]).union(*listaTotal[1:])
num_total_elements = len(total_elements) 

# Calculate the percentage similarity
percentage_similarity = (float(num_common_elements) / float(num_total_elements)) * 100

# printing result
print("Results from "+ str(ini) + " to "+str(fin) + " when the modularity is bigger than 0.60. (Using only the bigger communitys in every hour)")
print("number of temporal points : " + str(cont))
print("number of common elements in all lists : " + str(num_common_elements))
print("total number of unique elements in all lists : " + str(num_total_elements))
print("Percentage similarity among lists is : {:.2f}".format(percentage_similarity))
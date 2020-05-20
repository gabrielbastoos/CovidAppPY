#reading api from github.com/turicas/covid19

import requests
import json
import matplotlib
from scipy.optimize import curve_fit
#ENV["MPLBACKEND"]="tkagg"
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import numpy as np

cidade = input("COVID INFORMA:\n Qual cidade?")

parametros = {
    #"state":"RJ"
    "city":cidade
    #"is_last":"True"
}

def exponential(x,a,b):
    return a*np.exp(b*x)

response = requests.get("https://brasil.io/api/dataset/covid19/caso/data", params=parametros)
print("Code Response of Request:"+str(response.status_code))
data = json.loads(json.dumps(response.json(), sort_keys=True, indent=4))
count = int(data['count'])
vetor=[]
vetor_morte =[]

for i in reversed(range(count)):
    vetor.append((data['results'][i]['confirmed']))
    vetor_morte.append((data['results'][i]['deaths']))
    print("Confirmados: "+str(data['results'][i]['confirmed'])+" Mortes: "+str(data['results'][i]['deaths']))


x_data = np.linspace(start=0,stop=count,num=count)
pars, cov = curve_fit(f=exponential,xdata=x_data,ydata=vetor,p0=[0,0])
fig, ax = plt.subplots()
print("População estimada 2019:"+str(data['results'][count-1]['estimated_population_2019']))
print("Porcentagem da população:"+str(round(100*vetor[count-1]/data['results'][count-1]['estimated_population_2019'],3))+"%")
ax.plot(x_data,exponential(x_data,*pars),linestyle='--',linewidth=2,color='red',label="Exponential Fit")
ax.plot(vetor, label="Confirmados")
ax.plot(vetor_morte,label="Mortes")
ax.legend()
#print("Parâmetros do fit:"+str(pars))
plt.show()

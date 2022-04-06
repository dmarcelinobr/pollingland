#!/usr/bin/env conda polls

# inicio
import sys
import os
try:
	import warnings                                                   
	warnings.filterwarnings('ignore')     
	import pandas as pd       
	import numpy as np
	import sqlite3
	import watermark
	import pymc3 as pm
	import xarray as xr
	import arviz as az
	import theano.tensor as aet
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdates
	import matplotlib.cbook as cbook
	from scipy.special import expit as logistic
	from IPython.display import display, HTML
	from dateutil.relativedelta import relativedelta
	
except ImportError:
	print("Error: missing one of the libraries..")
	sys.exit()
	
sys.path.append('../..')

from manager_db import *
from model_utils import *

# hide
RANDOM_SEED = 8927
np.random.seed(RANDOM_SEED)
az.style.use("arviz-darkgrid")

print(os.getcwd())
print(sys.argv[0])
print(os.path.dirname(os.path.realpath('__file__')))
print('Running on pymc3 v{}'.format(pm.__version__))
print('Running on arviz v{}'.format(az.__version__))


"""
JOTA polls of polls model
Daniel Marcelino, June, 2021
: run the code in the terminal window with
: "python jota_vote_intention.py"
: requires package: pymc3
"""


# SQL database connection

con = sqlite3.connect('../../pollingpoint.db')

file_long = pd.read_sql(""" SELECT data_ini, data_fim, nome, empresa, cargo,
turno, candidato, voto, erro, amostra, tipo, modo FROM intencao
ORDER BY data_fim;""", con=con) 

con.close()

# Data transformation
#
## Converte para datetime 
file_long["date"] = pd.to_datetime(file_long["data_fim"])

## Index by field date
file_long.set_index("date", inplace=True)

## sort by field date
file_long = file_long.sort_index(axis=0)

## extrair date informacation 
file_long['day'] = file_long.index.day
file_long['month'] = file_long.index.month
file_long['week'] = file_long.index.week
file_long['year'] = file_long.index.year

## Replace NA with 1000 interviews 
file_long["amostra"] = file_long["amostra"].replace(np.nan, 1000)

## Convert vote intention rates to proportion 
file_long[["voto", "erro"]] = (file_long[["voto", "erro"]].copy()/100)

## Gerar inteiros a partir das médias 
file_long["num_voto"] = np.floor(file_long["amostra"] * (file_long["voto"])).astype("int")

## Reset the index
file_long = file_long.reset_index().rename(columns={"index": "date"})

print("<h1 style='color:red'>First summary table</h1>")


print(file_long.groupby(by=['data_ini', 'data_fim', 'empresa'],as_index=False).count())


# Data checks/validation
print(file_long.groupby(by=['date', 'empresa'],as_index=False).count())


print(file_long.groupby(by=['candidato'],as_index=False).count())


print(file_long.groupby(by=['tipo'],as_index=False).count())


pd.crosstab(file_long.year, file_long.tipo, margins=True)


pd.crosstab(file_long.year, file_long.turno, margins=True)

pd.crosstab(file_long.year, file_long.month, margins=True)


# file_long1t = file_long.loc[(file_long['turno'] == 1) & (file_long['tipo'] == 'Intenção')]

file_long1t = file_long[file_long['turno'] == 1]

# Descritiva
file_long1t.groupby('candidato').voto.agg(
	voto_max=('max'),
	voto_min=('min'),
	voto_media=('mean'),
	).round(2)*100
	
	
	
file_long2t = file_long[file_long['turno'] == 2]

# Descritiva
file_long2t.groupby('candidato').voto.agg(
	voto_max=('max'),
	voto_min=('min'),
	voto_media=('mean'),
	).round(2)*100.
	



media_1t = file_long1t.pivot_table(index=["data_fim","empresa", "turno", "modo"], 
					columns='candidato', 
					values='voto',
					margins=True,   # add margins
					aggfunc='mean') # sum margins(rows/columns)


media_2t = file_long2t.pivot_table(index=["data_fim","empresa", "turno", "modo"], 
					columns='candidato', 
					values='voto',
					margins=True,   # add margins
					aggfunc='mean') # sum margins(rows/columns)
				
				
				
				
file_wide = file_long1t.pivot_table(index=["empresa", "turno", "modo", "tipo"], 
					columns='candidato', 
					values='voto')

# Tabela pronta para análise:
file_wide.query("tipo == 'Estimulada'| tipo == 'Estimulada' | tipo == 'Intenção'")



# Query para filtrar dados de interesse: 1 turno e pesquisas de intenção de votos apenas
file_long_sub = file_long.query("tipo == 'Estimulada' | tipo == 'Intenção' & turno==1")



data = file_long_sub.pivot_table(index=['date', 'data_fim', 'day', 'month', 'year', 'empresa', 'turno', 'tipo', 'modo', 'amostra'], 
					columns=['candidato'], 
					values='voto').reset_index()

data["Bolsonaro"] = data.groupby(["year", "month"])["Bolsonaro"].transform(lambda x: x.fillna(method='ffill'))
data["Lula"] = data.groupby(["year", "month"])["Lula"].transform(lambda x: x.fillna(method='ffill'))
data["Ciro"] = data.groupby(["year", "month"])["Ciro"].transform(lambda x: x.fillna(method='ffill'))
data["Moro"] = data.groupby(["year", "month"])["Moro"].transform(lambda x: x.fillna(method='ffill'))

data["Bolsonaro"] = data.groupby(["year", "month"])["Bolsonaro"].transform(lambda x: x.fillna(method='bfill'))
data["Lula"] = data.groupby(["year", "month"])["Lula"].transform(lambda x: x.fillna(method='bfill'))
data["Ciro"] = data.groupby(["year", "month"])["Ciro"].transform(lambda x: x.fillna(method='bfill'))
data["Moro"] = data.groupby(["year", "month"])["Moro"].transform(lambda x: x.fillna(method='bfill'))

POLLSTERS = data["empresa"].sort_values().unique()
comment = f"""A base de pesquisas contaim {len(data)} pesquisas realizadas entre {data["year"].min()} e {data["year"].max()}.
Existem {len(POLLSTERS)} empresas de pesquisa: {', '.join(list(POLLSTERS))}
"""
print(comment)

# display(HTML(data.to_html()))



# Query para filtrar dados de interesse: 1 turno e pesquisas de intenção de votos apenas
file_long_sub = file_long.query("tipo == 'Estimulada' | tipo == 'Intenção' & turno==1")


# Converte para datetime 
file_long_sub["date"] = pd.to_datetime(file_long_sub["date"])

# Index by field date
file_long_sub.set_index("date", inplace=True)


data = file_long_sub.groupby(["candidato", "empresa"]).resample("W").mean().reset_index(level=0).sort_index()

print(data)



# time = dates_to_idx(file_long_sub.index)
# time[:10]

# Models 
## Bolsonaro


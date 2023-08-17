#==========================================================================================================
#------------------------------PROJETO DO ALUNO FTC - ANALISANDO DADOS EM PYTHON---------------------------
#==========================================================================================================

#-------------------------------------------VISÃO CIDADES--------------------------------------------------



#==========================================================================================================
#-------------------------------------------BIBLIOTECAS----------------------------------------------------
#==========================================================================================================

import pandas as pd #biblioteca para tratamento dos dados
import plotly as pl #biblioteca para plotarmos os graficos
import haversine as hs #biblioteca para fazermosa o calculo da localização dos restaurantes usando as coordenadas disponibilizadas
import inflection #biblioteca com diversas funções para fazermos mudanças em strings, por exemplo, converter de letra maiscuila para minuscula e etc...
import numpy as np
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from PIL import Image


#====================Icone da pagina========================================
st.set_page_config(
    page_title="Cidades",
    page_icon="🌆"
)
#====================Icone da pagina========================================


#==========================================================================================================
#-------------------------------------------FUNÇÕES--------------------------------------------------------
#==========================================================================================================

#---------------- Função para criarmos uma coluna com o nome dos paises baseados pelo código disponibilizado ----------------------#

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]
    
#---------------------Função para criar  a categoria do  tipo de custo do restaurante-----------------------#    

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#---------------------Função para criação do nome das cores----------------------------------#

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


#---------------------Função para renomear o nome das colunas do DataFrame-------------------#

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x) #função da biblioteca inflection que substitui caracteres
    snakecase = lambda x: inflection.underscore(x) #função da biblioteca inflection que substitui um determinado caractere por underscore (underline)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#==========================================================================================================
#-------------------------------------------EXTRACT--------------------------------------------------------
#==========================================================================================================

path_file = 'C:/Users/EngKa/Documents/repos/pa_ftc/train.csv'
df = pd.read_csv(path_file)
df1 = df.copy()

#==========================================================================================================
#-------------------------------------------TRANSFORM------------------------------------------------------
#==========================================================================================================

#-------------------------------Aplicando as funções-----------------------------------------#    
    
#utilizando a função para renomear e substituir espaço por underline
df1 = rename_columns(df1) 

#--------------utilizando a função para criar a coluna com o nome dos países baseado nos códigos e na função country_name-----------#

country_code = list(df1['country_code'])
a=0
for valores in country_code:
    country_code[a] = country_name(valores)
    a=a+1
df1['country'] = country_code

#--------------Criando a coluna com os nomes das cores da avaliação--------------------------#

rating_color = list(df1['rating_color'])
a=0
for valor in rating_color:
    rating_color[a] = color_name(valor)
    a = a+1
df1['color_rating_name'] = rating_color

#-----------------Criando a coluna com os nomes dos tipos de preço de comida (barato, normal e etc)----------------------------#

new_price_type = list(df1['price_range'])
a = 0
for valor in new_price_type:
    new_price_type[a] = create_price_type(valor)
    a = a + 1
df1['price_type'] = new_price_type

df1.head(5)

#-------------------Deixando as linhas da coluna 'cuisines' com apenas um tipo de culinaria, conforme solicitado------------------#

df1 = df1.dropna() #utilizado para remover as linhas do dataframe que não possuem valores.

df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0]) #a função apply foi utilizada para removermos todos os valores depois 
#das colunas cuisines, para mantermos apenas o primeiro tipo de culinaria conforme solicitado

df1.head(2) #Verificando se as alterações feitas surtiram efeitos

#==========================================================================================================
#-------------------------------------------LAYOUT STREAMLIT-----------------------------------------------
#==========================================================================================================

st.markdown('# Visão de negócio: Cidades')
st.markdown('##### Abaixo você encontrará informações úteis para tomadas de decisões do negócio com base nas cidades:')


#==========================================================================================================
#-------------------------------------------SIDEBAR--------------------------------------------------------
#==========================================================================================================

# image_path='C:/Users/EngKa/Documents/repos/pa_ftc/zomato.png'
image = Image.open('zomato.png')
st.sidebar.image( image, width=280 )

st.sidebar.markdown('# Seja bem vindo(a) a Zomato Restaurants')
st.sidebar.write("""---""")

st.sidebar.markdown('## Selecione os países que deseja analisar:')
country_options = st.sidebar.multiselect(
    'Selecione os países:',
    ['India','Australia','Brazil','Canada',
     'Indonesia','New Zeland','Philippines','Qatar',
     'Singapure','South Africa','Sri Lanka','Turkey',
     'United Arab Emirates','England','United States of America'],
    default=['India','Australia','Brazil','Canada','England','United States of America'])

st.sidebar.write("""---""")
st.sidebar.write('Powered By: Kaique Dias')


#---------------------------------ATIVAÇÃO DOS FILTROS DO SIDEBAR------------------------------------------

paises_selecionados = df1['country'].isin(country_options)
df1 = df1.loc[paises_selecionados,:]

#==========================================================================================================
#-------------------------------------------MAINPAGE-------------------------------------------------------
#==========================================================================================================

#------------------------------------------------CONTAINER SUPERIOR-------------------------------------------------------------------
with st.container():
    colunas = ['city', 'restaurant_id','country']
    df2 = df1.loc[:,colunas].groupby(['city', 'restaurant_id','country']).count().reset_index()
    df3 = df2.loc[:,colunas].groupby(['city','country']).count().sort_values('restaurant_id',ascending=False).reset_index()
    df3 = df3.head(20)    
    fig = px.bar(df3, x = 'city', y = 'restaurant_id', color = 'country', labels = {'restaurant_id':'Total de Restaurantes','city':'Cidade','country':'País'}, title = 'Top 10 cidades com mais Restaurantes Cadastrados')
    st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------CONTAINER MEIO-----------------------------------------------------------------------

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        filtro = df1['aggregate_rating'] >= 4.0
        df2 = df1.loc[filtro,['restaurant_id','city','aggregate_rating','country']].groupby(['restaurant_id','country','city']).nunique().sort_values('aggregate_rating', ascending=False).reset_index()       
        df3 = df2.loc[:,['country','city','aggregate_rating']].groupby(['city','country']).count().sort_values('aggregate_rating', ascending=False).reset_index()
        df3 = df3.head(7)
        fig = px.bar(df3, x = 'city' , y = 'aggregate_rating' , color = 'country', labels = {'aggregate_rating':'Total de Restaurantes','city':'Cidade','country':'País'}, title='Top 7 cidades com média de avaliação Superior a 4.0')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        filtro = df1['aggregate_rating'] <= 2.5
        df2 = df1.loc[filtro,['restaurant_id','city','aggregate_rating','country']].groupby(['restaurant_id','country','city']).count().sort_values('aggregate_rating', ascending=False).reset_index()        
        df3 = df2.loc[:,['country','city','aggregate_rating']].groupby(['city','country']).count().sort_values('aggregate_rating', ascending=False).reset_index()
        df3 = df3.head(7)               
        fig = px.bar(df3, x = 'city' , y = 'aggregate_rating' , color = 'country', labels = {'aggregate_rating':'Quantidade de Restaurantes','city':'Cidade','country':'País'}, title = 'Top 7 cidades com média de avaliação inferior a 2.5')        
        st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------CONTAINER INFERIOR-----------------------------------------------------------------------

with st.container():
    colunas = ['city','cuisines','country']
    df2 = df1.loc[:,colunas].groupby(['city','cuisines','country']).nunique().sort_values('cuisines',ascending=False).reset_index()    
    colunas_1 = ['city','cuisines','country']
    df3 = df2.loc[:,colunas_1].groupby(['city','country']).count().sort_values('cuisines',ascending=False).reset_index()
    df3 = df3.head(10)
    fig = px.bar(df3, x = 'city', y = 'cuisines', color = 'country', labels = {'city':'Cidade','cuisines':'Tipos de Culinária','country':'País'}, title = 'Top 10 cidades com a maior variedade de Restaurantes de Culinárias diferentes' )
    st.plotly_chart(fig, use_container_width=True)
        

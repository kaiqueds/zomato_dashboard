#==========================================================================================================
#------------------------------PROJETO DO ALUNO FTC - ANALISANDO DADOS EM PYTHON---------------------------
#==========================================================================================================

#-----------------------------------------VISÃO COZINHAS---------------------------------------------------



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
    page_title="Cozinhas",
    page_icon="🍽️"
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

dfc = df1.copy() # DATAFRAME CRIADO PARA OS FILTROS NÃO INFLUENCIAREM NO RESULTADO APRESENTADO NO CONTAINER DOS MELHORES RESTAURANTES.


#==========================================================================================================
#-------------------------------------------LAYOUT STREAMLIT-----------------------------------------------
#==========================================================================================================

st.markdown('# Visão de negócio: Culinárias')
st.markdown('##### Abaixo você encontrará informações úteis para análise do negócio baseado nos tipos de culinárias:')


#==========================================================================================================
#-------------------------------------------SIDEBAR--------------------------------------------------------
#==========================================================================================================

# image_path='C:/Users/EngKa/Documents/repos/pa_ftc/zomato.png'
image = Image.open('zomato.png')
st.sidebar.image( image, width=280 )

st.sidebar.markdown('## Olá, seja bem vindo a Zomato Restaurants')
st.sidebar.write("""---""")

st.sidebar.markdown('## Selecione os países que deseja analisar:') #ABAIXO 
country_options = st.sidebar.multiselect(
    'Selecione os países:',
    ['India','Australia','Brazil','Canada',
     'Indonesia','New Zeland','Philippines','Qatar',
     'Singapure','South Africa','Sri Lanka','Turkey',
     'United Arab Emirates','England','United States of America'],
    default=['India','Australia','Brazil','Canada','England','United States of America'])

st.sidebar.write("""---""")

st.sidebar.markdown('## Selecione a quantidade de dados que deseja visualizar:')
qtd_restaurantes = st.sidebar.select_slider('Quantidade:', 
                 options=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], value=(20))
# ,format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")

st.sidebar.write("""---""")
st.sidebar.write('Powered By: Kaique Dias')


#---------------------------------ATIVAÇÃO DOS FILTROS DO SIDEBAR------------------------------------------

paises_selecionados = df1['country'].isin(country_options) #FILTRO MULTISELECT
df1 = df1.loc[paises_selecionados,:]#FILTRO MULTISELECT

restaurantes = qtd_restaurantes


#==========================================================================================================
#-------------------------------------------MAINPAGE-------------------------------------------------------
#==========================================================================================================

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap='small')
    with col1: #Top restaurante italiano
        filtro = dfc['cuisines'] == 'Italian'
        colunas = ['restaurant_id','restaurant_name','aggregate_rating']
        df2 = dfc.loc[filtro,colunas].groupby(['restaurant_id']).max().sort_values('aggregate_rating',ascending=False).reset_index()
        filtro = df2['aggregate_rating'] >= 4.9
        df2 = df2.loc[filtro,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        italiana = df2.iloc[0,1]
        col1.metric('Top Rest Italiano:', italiana)

    with col2: #Top restaurante fast-food
        filtro = dfc['cuisines'] == 'Fast Food'
        colunas = ['restaurant_id','restaurant_name','aggregate_rating']
        df3 = dfc.loc[filtro,colunas].groupby(['restaurant_id']).max().sort_values('aggregate_rating',ascending=False).reset_index()
        filtro = df3['aggregate_rating'] >= 4.9
        df3 = df3.loc[filtro,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        fast_food = df3.iloc[0,1]
        col2.metric('Top Fast-Food:', fast_food)
                
    with col3: #Top restaurante japones
        filtro = dfc['cuisines'] == 'Japanese'
        colunas = ['restaurant_id','restaurant_name','aggregate_rating']
        df4 = dfc.loc[filtro,colunas].groupby(['restaurant_id']).max().sort_values('aggregate_rating',ascending=False).reset_index()
        filtro = df4['aggregate_rating'] >= 4.9
        df4 = df4.loc[filtro,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        japonesa = df4.iloc[0,1]
        col3.metric('Top Rest Japonês:', japonesa)
        
    with col4: #Top restaurante arabe
        filtro = dfc['cuisines'] == 'Arabian'
        colunas = ['restaurant_id','restaurant_name','aggregate_rating']
        df5 = dfc.loc[filtro,colunas].groupby(['restaurant_id']).max().sort_values('aggregate_rating',ascending=False).reset_index()
        filtro = df5['aggregate_rating'] >= 4.7
        df5 = df5.loc[filtro,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        arabe = df5.iloc[0,1]
        col4.metric('Top Rest Árabe:', arabe)
        
    with col5: #Top restaurante bbq
        filtro = dfc['cuisines'] == 'BBQ'
        colunas = ['restaurant_id','restaurant_name','aggregate_rating']
        df6 = dfc.loc[filtro,colunas].groupby(['restaurant_id']).max().sort_values('aggregate_rating',ascending=False).reset_index()
        df6 = df6.loc[:,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        filtro = df6['aggregate_rating'] >= 4.9
        df6 = df6.loc[filtro,:].groupby(['restaurant_id']).max().sort_values('restaurant_id',ascending=True).reset_index()
        bbq = df6.iloc[0,1]
        col5.metric('Top Rest Barbecue:', bbq)

with st.container():
    filtro = df1['aggregate_rating'] >= 4.9
    colunas = ['restaurant_name','cuisines','city','aggregate_rating','votes']    
    df2 = df1.loc[filtro,colunas].groupby(['restaurant_name']).max(['aggregate_rating','votes']).sort_values('votes',ascending=False).reset_index()
    df3 = df2.head(restaurantes)
    st.markdown(f'#### Top {qtd_restaurantes} Restaurantes:')
    st.dataframe(df3, use_container_width=True)
    
with st.container():
    filtro = df1['aggregate_rating'] >= 4.9
    colunas = ['cuisines','aggregate_rating']    
    df2 = df1.loc[filtro,colunas].groupby(['cuisines']).max().sort_values('aggregate_rating',ascending=False).reset_index()
    df2 = df2.head(restaurantes)       
    fig = px.bar(df2, x='cuisines', y='aggregate_rating', labels = {'aggregate_rating':'Avaliação Média','cuisines':'Culinária'})
    st.markdown(f'#### Top {qtd_restaurantes} Melhores Culinárias:')
    st.plotly_chart(fig, use_container_width = True)


with st.container():
    filtro = df1['aggregate_rating'] <= 2.5
    colunas = ['cuisines','aggregate_rating']    
    df2 = df1.loc[filtro,colunas].groupby(['cuisines']).max().sort_values('aggregate_rating',ascending=False).reset_index()
    df2 = df2.head(restaurantes)    
    fig = px.bar(df2, x='cuisines', y='aggregate_rating', labels = {'aggregate_rating':'Avaliação Média','cuisines':'Culinária'})
    st.markdown(f'#### Top {qtd_restaurantes} Piores Culinárias:')
    st.plotly_chart(fig, use_container_width = True)
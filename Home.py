import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)


# image_path = 'Documents/repos/dashboards/logo.png' =========> Não estou conseguindo fazer com que abra pelo arquivo

# image_path='C:/Users/EngKa/Documents/repos/pa_ftc/zomato.png'
image = Image.open('zomato.png')
st.sidebar.image( image, width=280 )

st.sidebar.markdown( '# Zomato Restaurants' )
st.sidebar.markdown( '### Seja bem vindo(a) ao estudo dos dados da empresa Zomato Restaurants' )
st.sidebar.markdown( """---""" )

st.write( "# Zomato Restaurants Data Dashboard" )

st.markdown(
""" Seja bem vindo ao Dashboard dinâmico da empresa Zomato Restaurants,
    este dashboard foi construído para o acompanhamento das métricas da empresa baseado em 4 visões importantes para o negócio: Visão Geográfica, Visão Paises, Visão Cidades e Visão Cozinhas.

    ### Sobre a Zomato: 
    A zomato é um serviço de busca de restaurantes e delivery, ela atua em diversos países da Ásia, Europa e alguns páises na américa, ela foi fundada em julho de 2008 com o intuito de ajudar os clientes a encontrarem restaurantes que atendessem suas necessidades, se tornando um excelente lugar para empresas do segmento de restaurantes ficarem expostas para seus clientes, potencializando seus resultados.

    ### Fonte dos dados:
    Os dados utilizados no estudo e construção deste dashboard foram disponibilizados na plataforma Kaggle, sendo assim, os dados ficaram publicos para qualquer pessoa utilizá-los em suas analises. O link para download dos arquivos é: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv . É  importante salientar que este dataset é de anos atrás, portanto, as informações e resultados das analises estão desatualizados, a empresa Zomato cresceu e hoje atua em mais países e cidades além das apresentadas aqui.
    
    ### Como utilizar esse Dashboard?
    - Visão Geográfica:    
        - Acompanhamento da distribuição geográfica dos restaurantes, clusterizado por regiões (continentes, países e cidades)     
    - Visão Países:    
        - Acompanhamento dos indicadores de crescimento dos restaurantes e satisfação dos clientes.       
    - Visão Cidades: 
        - Acompanhamento dos indicadores dos restaurantes, as cidades com mais restaurantes cadastrados, as com melhor média de avaliação e etc.
    - Visão Cozinhas:
        - Acompanhamento dos melhores e piores restaurantes e culinárias
    ### Ask for Help - Entre em contato com o desenvolvedor:
    - Discord: kaiquedias
    - Email: eng.kaique@outlook.com
    - LinkedIn: https://www.linkedin.com/in/kaique-faustino-dias-40321390/
    - GitHub: https://github.com/kaiqueds
"""
)

#st.sidebar.markdown( """---""" )

st.sidebar.markdown('### Powered by Kaique Dias')
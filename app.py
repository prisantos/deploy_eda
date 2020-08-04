
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd 
import altair as alt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def sobre(): 
    st.sidebar.subheader('Priscilla Nascimento Santos' )
    #st.sidebar.image('image.jpg', width=40, use_column_width=True )
    st.sidebar.subheader('Sobre mim:') 
    st.sidebar.markdown('Mestre em Informática, Cientista de dados e Apaixonada pela Educação! ')
    #subtitulo 
    st.sidebar.markdown('[Linkedin](https://www.linkedin.com/in/priscilla-nascimento-santos-418aaa48/)')
    st.sidebar.markdown('[Github](https://github.com/prisantos)')

def criar_histograma(coluna, df):
    histograma = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin= True), 
        y = 'count()', tooltip = [coluna, 'count()']
    ).interactive()
    return histograma 

def criar_barras (coluna_num, coluna_cat, df):
    barras = alt.Chart(df, width=600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return barras

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df,width= 600).mark_boxplot().encode(
        x = coluna_num, 
        y= coluna_cat
    ) 
    return boxplot

def criar_Scatterplot(x,y, df):
    scatter = alt.Chart (df, width=600, height=400).mark_circle().encode(
        alt.X (x), 
        alt.Y(y), 
        tooltip = [x,y]
    ).interactive()
    return scatter 

def matriz_correlacao (numero):
    st.markdown('Matriz de Correlação.')
    opcoes_correlacao = st.multiselect('Escolha as variáveis:', list(numero.columns), default=list(numero.columns))
    correlacao = st.radio('Escolha o método de correlação', ('Pearson','Spearman','Kendall'))
    corr = numero[opcoes_correlacao].corr(method=correlacao[0].lower() + correlacao[1:])
    if (opcoes_correlacao  == 0):
        opcoes_correlacao = list(numero)
    if correlacao =='Person':
        st.markdown('Método de Correlação de Person')
    if correlacao == 'Spearman':
        st.markdown('Método de Correlação de Spearman')
    if correlacao == 'Kendall':
        st.markdown('Método de Correlação de Kendall')
    st.markdown('**Tabela de Correlação**')
    st.write(corr)
    st.markdown('**Matriz de Correlação**')
    st.write('Para grande bases de dados a matriz de correlação pode ser mais adequada.')
    sns.heatmap(corr, fmt='.2f', square=True, annot=True)
    st.pyplot()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def nuvem_palavras (coluna_cat):
    resumo = "Priscilla, priscilla"
    #concatenar as palavras
    # lista de stopword
    stopwords = set(STOPWORDS)
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os"])
    wordcloud = WordCloud(stopwords=stopwords,
                      background_color='black', width=1000,                            
                      height=1000).generate(resumo)
    fig, ax = plt.subplots(figsize=(16,8))            
    ax.imshow(wordcloud, interpolation='bilinear')       
    ax.set_axis_off()
    plt.imshow(wordcloud)
    st.pyplot()


def main():
    #titulo
    st.title('Data Science')
    st.write('Esta página é dedicada ao desenvolvimento de uma aplicação para Análise de Dados', 
             'utilizando o Streamlit')
    
    df = st.file_uploader('Escolha a base de dados que deseja analisar (.csv)', type='csv') #IMPORTANDO AS BASES 
    
    

    if df is not None: 


        df = pd.read_csv(df, index_col=False)
        opcao = ('Análise Exploratória', 'Visualização dos dados')
        st.sidebar.title('Escolha o tipo de Análise')
        sidebar_Opcao = st.sidebar.radio('', opcao)

        st.subheader(sidebar_Opcao)
        
        #criando uma dataframe aux 
        
        df_aux = pd.DataFrame({"colunas": df.columns, 'Tipos': df.dtypes, 'Nulos #': df.isna().sum(),
                            'Nulos %': (df.isna().sum() / df.shape[0]) * 100})
        colunas_numericas  = list(df_aux[df_aux['Tipos'] != 'object']['colunas'])
        colunas_categoricas =  list(df_aux[df_aux['Tipos'] == 'object']['colunas'])
        
        # Montando o Sidebar 
        if (sidebar_Opcao == 'Análise Exploratória'):
            st.markdown ('** Analisando o DataFrame **')
            st.write('O arquivo de sua base de dados possui ', df.shape[0],' linhas e ', df.shape[1],' colunas.')
            st.markdown('**Visualizando o Dataframe**')
            numero_linhas = st.slider('Escolha o numero de linhas que deseja ver', min_value=2, max_value=100)
            st.dataframe(df.head(numero_linhas))
            st.write('Você selecionou: ', numero_linhas, 'linhas.')
            st.markdown ('**Tipo de Variáveis:**')
            valores = pd.DataFrame({'Colunas': df.columns, 'Tipos': df.dtypes, 'Valores Nulos': df.isna().sum(), 
                                    'Nulos %': (df.isna().sum() / df.shape[0]) * 100}) 
            st.write(valores) 

            #variaveis numericas 
            st.write ('**Variáveis Numéricas**')

           
            st.table(df[colunas_numericas]. describe().transpose())

            #variaveis categoricas 
            st.write('**Variáveis Categóricas**')
            st.table(df[colunas_categoricas]. describe().transpose())

            #visualizando valores únicos 
            st.markdown('**Visualização de valores únicos:**')
            unicos = st.selectbox ('Escolha uma coluna', df.columns)
            st.dataframe (pd.DataFrame({unicos: df[unicos].unique()}))


            st.markdown('**Estatística descritiva univariada**')
            coluna = st.selectbox('Selecione a coluna :', colunas_numericas[1:])
            if coluna is not None:
                st.markdown ('Selecione o que deseja analisar :')
                media = st. checkbox('Média')
                if media: 
                    st.markdown (df[coluna].mean())
                mediana = st.checkbox('Mediana')
                if mediana: 
                    st.markdown (df[coluna]. median())
                desvio_padrao = st.checkbox('Desvio Padrão')
                if desvio_padrao:
                    st.markdown (df[coluna]. std())
                kurtosis = st. checkbox('Kurtosis')
                if kurtosis: 
                    st.markdown (df[coluna]. kurtosis())
                skewness = st. checkbox('Skewness')
                if skewness: 
                    st.markdown (df[coluna]. skew())

            st.markdown('**Matriz de Correlação**')
            matriz_correlacao(df[colunas_numericas])

        if (sidebar_Opcao == 'Visualização dos dados'):
            opcao_graficos = ('Histograma', 'Barras', 'Boxplot', 'ScatterPlot', 'Word Cloud')
            st.sidebar.title('Escolha o tipo de Gráfico:')
            sidebar_graficos = st.sidebar.radio('', opcao_graficos)

            if (sidebar_graficos == 'Histograma'):
                st.markdown ('Histograma')
                coluna = st.selectbox('Selecione a Coluna Numérica:', colunas_numericas[1:])
                st.markdown('Histograma da coluna: ' + str(coluna))
                st.write(criar_histograma(coluna,df))

            elif (sidebar_graficos == 'Barras'):
                st.markdown('Barras')
                coluna_num = st.selectbox('Selecione a Coluna Numérica:', colunas_numericas[1:])
                coluna_cat = st.selectbox ('Selecione a Coluna Categórica:', colunas_categoricas[0:])
                st.markdown('Gráfico de Barras da Coluna: ' + str(coluna_num) + 'pela coluna:' + str(coluna_cat))
                st.write(criar_barras(coluna_num, coluna_cat,df))

            elif (sidebar_graficos == 'Boxplot'):
                st.markdown('**Boxplot**')
                coluna_num = st.selectbox('Selecione a Coluna Numérica:', colunas_numericas[1:])
                coluna_cat = st.selectbox('Selecione a Coluna Categórica:', colunas_categoricas[0:])
                st.markdown('Gráfico de Boxplot : ' + str(coluna_num) + 'pela coluna:' + str(coluna_cat))
                st.write (criar_barras (coluna_num, coluna_cat, df))

            elif (sidebar_graficos == 'ScatterPlot'): 
                st.markdown ('**ScatterPlot**')
                coluna_num = st.selectbox('Selecione a Coluna Numérica:', colunas_numericas[1:])
                coluna_cat = st.selectbox('Selecione a Coluna Categórica:', colunas_categoricas[0:])
                st.markdown('Gráfico de ScatterPlot: ' + str(coluna_num) + 'pela coluna:' + str(coluna_cat))
                st.write (criar_Scatterplot (coluna_num, coluna_cat, df))

            elif(sidebar_graficos=='Word Cloud'):
                st.markdown('**Word Cloud: Nuvem de Palavras**')
                coluna_cat = st.selectbox('Selecione a Coluna Categórica:', colunas_categoricas[0:])
                st.markdown('Nuvem de Palavras : ' + str(coluna_cat))
                st.write (nuvem_palavras (coluna_cat))


    else:  
        sobre()    



            


    

if __name__ == '__main__':
    main()

   
    
    
    

   
    
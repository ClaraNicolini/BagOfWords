import numpy as np
import pandas as pd 
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import itertools

nltk.download('stopwords')
stop = None
df = None
vectorizer = None
X = None

class BOW:
    def __init__(self):
        # Ajustando as opções do pandas para exibir todos os dados sem truncar
        pd.set_option('display.max_columns', None)  # Mostra todas as colunas
        pd.set_option('display.max_rows', None)     # Mostra todas as linhas
        pd.set_option('display.max_colwidth', None) # Mostra todo o conteúdo da coluna, sem truncar
        pd.set_option('display.expand_frame_repr', False)  # Evita que a exibição do DataFrame se quebre em várias linhas
        
        self.df = pd.read_csv('Data/IMDB Movies Dataset top 1000 complete.csv')
        self.stop = set(stopwords.words('english'))
        self.combine_columns()
        self.clear_content()
        self.create_BOW()
        

    def combine_columns(self):
        # Criar uma nova série a partir da lista de titulos de serie/filme
        titles_list = pd.Series(self.df['Series_Title'].tolist())
        new_titles_column = pd.Series(titles_list)
        new_titles_column = new_titles_column.reindex(self.df.index, fill_value=None)

        # Criar uma nova série a partir da lista de directores
        directors_list = pd.Series(self.df['Director'].tolist())
        new_directors_column = pd.Series(directors_list)
        new_directors_column = new_directors_column.reindex(self.df.index, fill_value=None)
        # Adicionar ao DataFrame
        self.df['combined'] = new_titles_column + ' '+ new_directors_column + ' ' + self.df['Overview'].tolist()
        #print(self.df['combined'])


    def clear_content(self):
        # limpar a base removendo pontuações do campo overview que será nosso target
        self.df["combined"] = self.df["combined"].apply(lambda s: ' '.join(re.sub("[.,!?:;-='...\"@#_]", "", s).split()))
        # Remove as stopwords do texto da coluna target Overview
        self.df["combined"] = self.df["combined"].apply(lambda s: self.rem_en(s))
        # Tokenization
        tokeniser = RegexpTokenizer('\s+', gaps = True)
        self.df["combined"] = self.df["combined"].apply(lambda x: tokeniser.tokenize(x))
        # Normalização de palavras
        lemmatiser = WordNetLemmatizer()
        self.df["combined"] = self.df["combined"].apply(lambda tokens: [lemmatiser.lemmatize(token, pos='v') for token in tokens])


    # Criação do Bag of Words
    def create_BOW(self):
        # faz o join
        self.df['combined'] = self.df['combined'].apply(lambda x: ' '.join(x))

        # Instanciar o vetorizer (CountVectorizer)
        self.vectorizer = CountVectorizer(stop_words=None)  # Caso você já tenha removido as stop words

        # Ajustar o vetorizer ao texto e transformar as strings em vetores
        self.X = self.vectorizer.fit_transform(self.df['combined'])

        # Criar um DataFrame da matriz gerada
        bag_of_words_df = pd.DataFrame(self.X.toarray(), columns=self.vectorizer.get_feature_names_out())

        # Criando uma variável alvo fictícia
        y = np.zeros(bag_of_words_df.shape[0])

        # Separando em treino e teste (80% treino, 20% teste)
        X_train, X_test, y_train, y_test = train_test_split(bag_of_words_df, y, test_size=0.2, random_state=42)

        # debug
        # Exibir os nomes das features (palavras únicas)
        #print("\nPalavras vetorizadas:")
        #print(vectorizer.get_feature_names_out())

        #print("\nMatriz de vetores completa:")
        #print(X.toarray())

    # remove as stop words
    def rem_en(self, input_txt):
        words = input_txt.lower().split()
        noise_free_words = [word for word in words if word not in self.stop] 
        noise_free_text = " ".join(noise_free_words) 
        return noise_free_text

    # Função para buscar filmes baseados em uma palavra-chave
    def search_movies(self, keyword):
        # Transformar a palavra-chave em vetor
        keyword_vector = self.vectorizer.transform([keyword])
        # Calcular similaridade do cosseno entre a palavra-chave e os resumos dos filmes
        similarity = cosine_similarity(keyword_vector, self.X)
        try:
            # Criar um DataFrame com as similaridades e os títulos dos filmes
            results = pd.DataFrame({
                'Title':self.df['Series_Title'],
                'Director':self.df['Director'],
                'Overview': self.df['Overview'],
                'Score': self.df['Meta_score'],
                'Similarity': similarity.flatten()
            })
            
        except ValueError as e:
            print(e)
            
        # Classificar os resultados pela similaridade maior que zero
        df_ = results[results['Similarity'] > 0].sort_values(by='Similarity', ascending=False)
        return df_


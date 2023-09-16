import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import pickle

# Carregando dados do arquivo CSV do Kaggle
# url = 'https://raw.githubusercontent.com/muzanpvp/IA_Atividade8/blob/main/diabetes_dados-de-treinamento.csv'
# -*- coding: utf-8 -*-
"""Diabetes-Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QxUKmKMmufLO-6zkaEVeHi6svt5GPgTO

Importação da base de dados
"""

# Carregando dados do arquivo CSV do Kaggle
url = 'https://raw.githubusercontent.com/muzanpvp/IA_Atividade8/blob/main/diabetes_dados-de-treinamento.csv'
# -*- coding: utf-8 -*-
base_Treinamento = pd.read_csv(url)

""" base de teste"""
url_teste = 'https://raw.githubusercontent.com/muzanpvp/IA_Atividade8/blob/main/diabete_teste.csv'
base_teste = pd.read_csv(url_teste)

"""base de treinos"""
url_treino = 'https://raw.githubusercontent.com/muzanpvp/IA_Atividade8/blob/main/diabete_treino.csv'
base_treino = pd.read_csv(url_treino)

"""Salvar os dados de treino e teste em arquivos diferentes"""

# Salvar os dados de treino e teste em arquivos diferentes
def salvar_dados_treino_teste(base_Treinamento):
    treino_df = base_Treinamento.iloc[:615]
    teste_df = base_Treinamento.iloc[615:]

    treino_df.to_csv('treino.csv', index=False)
    teste_df.to_csv('teste.csv', index=False)

# Visualização das relações entre os atributos
def visualizar_correlacao(base_Treinamento):
    corr_matrix = base_Treinamento.corr() 
    sns.clustermap(corr_matrix, annot=True, fmt=".2f")
    plt.title("Correlação entre atributos")
    plt.show()

# Visualizar contagem da classe 'Outcome'
def visualizar_contagem_outcome(base_Treinamento):
    sns.countplot(x=base_Treinamento['Outcome'])
    plt.show()

# Visualizar histogramas de atributos
def visualizar_histogramas(base_Treinamento):
    attributes_to_plot = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    for attribute in attributes_to_plot:
        plt.hist(x=base_Treinamento[attribute])
        plt.title(f'Histograma de {attribute}')
        plt.show()

# Separar atributos de classes
def separar_atributos_classes(base_Treinamento):
    attributes = base_Treinamento.iloc[:, :8]
    classes = base_Treinamento['Outcome']
    return attributes, classes

# Verificar valores nulos
def verificar_valores_nulos(attributes):
    null_counts = attributes.isnull().sum()
    return null_counts

# Normalizar os atributos racionais com diferentes scalers
def normalizar_atributos(attributes):
    scalers = {
        'QuantileTransformer': preprocessing.QuantileTransformer(),
        'MaxAbsScaler': preprocessing.MaxAbsScaler(),
        'Normalizer': preprocessing.Normalizer(),
        'StandardScaler': preprocessing.StandardScaler(),
        'MinMaxScaler': preprocessing.MinMaxScaler()
    }
    
    normalized_attributes = {}
    
    for scaler_name, scaler in scalers.items():
        normalized_data = scaler.fit_transform(attributes)
        normalized_attributes[scaler_name] = normalized_data
        
    return normalized_attributes

# Separar dados de treino e dados de teste
def dividir_dados_treino_teste(normalized_attributes, classes):
    x_train, x_test, y_train, y_test = train_test_split(normalized_attributes, classes, test_size=0.2, random_state=0, shuffle=False)
    return x_train, x_test, y_train, y_test

# Salvar dados de treino e teste normalizados em arquivo binário
def salvar_dados_binarios(x_train, y_train, x_test, y_test):
    with open('treino.pkl', mode='wb') as f:
        pickle.dump([x_train, y_train], f)

    with open('teste.pkl', mode='wb') as f:
        pickle.dump([x_test, y_test], f)

# Treinamento do neurônio perceptron e avaliação
def treinar_perceptron_e_avaliar(normalized_attributes, classes, x_test, y_test):
    modelo = Perceptron()
    modelo.fit(normalized_attributes, classes)

    # Acurácia do modelo
    accuracy = modelo.score(x_test, y_test) * 100
    print(f'Acurácia do modelo: {accuracy:.2f}%')

    pred = modelo.predict(x_test)
    print(f'Valores esperados: {y_test.values.tolist()}')
    print(f'Valores previstos: {pred.tolist()}')

    # Mostra a porcentagem de acertos
    accuracy_percent = accuracy_score(pred, y_test) * 100
    print(f'Porcentagem de acertos: {accuracy_percent:.2f}%')

# Função principal
def main():
    base_Treinamento = pd.read_csv('seu_arquivo.csv')  # Substitua 'seu_arquivo.csv' pelo caminho do seu arquivo

    # Exemplos de como chamar as funções
    salvar_dados_treino_teste(base_Treinamento)
    visualizar_correlacao(base_Treinamento)
    visualizar_contagem_outcome(base_Treinamento)
    visualizar_histogramas(base_Treinamento)
    
    attributes, classes = separar_atributos_classes(base_Treinamento)
    
    null_counts = verificar_valores_nulos(attributes)
    print(f'Contagem de valores nulos:\n{null_counts}')
    
    normalized_attributes = normalizar_atributos(attributes)
    
    x_train, x_test, y_train, y_test = dividir_dados_treino_teste(normalized_attributes['StandardScaler'], classes)
    
    salvar_dados_binarios(x_train, y_train, x_test, y_test)
    
    treinar_perceptron_e_avaliar(normalized_attributes['StandardScaler'], classes, x_test, y_test)

if __name__ == '__main__':
    main()
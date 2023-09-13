'''
    Leonardo Marques Ferreira - 11921BSI235
    Script que implementa o modelo vetorial, faz processamento usando a NLTK,
    encontra o top 5 documentos com maior grau de similaridade
    python3 n2.py ./vocabulario.txt ./diretorioDosTxts/ "consulta"
'''
from unidecode import unidecode
from glob import glob

import string
import math
import sys

import nltk

#caminho relativo dos arquivos .txt que serao lidos
arquivos = sys.argv[2] + "*.txt"
#caminho do vocabulario a ser lido
voc = sys.argv[1]
#consulta
consulta = sys.argv[3].split()

#download das stopwords
nltk.download('stopwords')

#funcao que le o arquivo e cria uma lista com as palavras
def read_file(file, wordList):
    for line in file:
        for word in line.split():
            wordList.append(word)
    file.close()

#funcao que usa o unidecode na lista para facilitar o tratamento (substituida)
def unide(wordList):
    i = 0
    listSize = len(wordList)
    while i < listSize:
        wordList[i] = unidecode(wordList[i]) #unide
        wordList[i] = wordList[i].translate(str.maketrans('','', string.punctuation)) #remove a pontuacao
        wordList[i] = wordList[i].lower() #letras minusculas
        i+=1

#funcao que faz o stemming usando o algoritmo de porter da NLTK
def porter_stemming(wordList):
    porter = nltk.PorterStemmer()
    wordListStem = []
    for word in wordList:
        wordListStem.append(porter.stem(word))
    return wordListStem

#funcao de pre processamento - retorna o documento (wordlist) convertido e sem stopwords
def pre_proc(wordList, stopwordsIdioma):
    wordListMin = wordList
    unide(wordListMin)
    wordListProc = []
    stopwords = set(nltk.corpus.stopwords.words(stopwordsIdioma))
    for word in wordListMin:
        for stopword in stopwords:
            if word != stopword:
                wordListProc.append(word)
    wordList = wordListProc

#funcao que le o txt do vocabulario e retorna a lista dos termos
def read_vocabulario(path):
    vocabulario = []
    arquivoDoVocabulario = open(path, 'rt')
    read_file(arquivoDoVocabulario, vocabulario)
    return vocabulario

#funcao que retorna um dicionario contendo os vetores TF de cada arquivo
def tf_table(vocabulario):
    listaDeArquivos = glob(arquivos) #lista de documentos
    dicionarioDocTermos = dict() #dicionario - {arquivo : vetorTFdoArquivo}
    for file in listaDeArquivos:
        vetorTf = []
        documento = []
        arquivoAtual = open(file, 'rt')
        read_file(arquivoAtual, documento)
        #unide(documento)
        pre_proc(documento, 'english') # ...
        #stemming
        documento = porter_stemming(documento)
        for termo in vocabulario:
            numeroDeAparicoes = documento.count(termo)
            if numeroDeAparicoes > 0:
                vetorTf.append(1.0 + math.log(numeroDeAparicoes, 2))
            else:
                vetorTf.append(0)
        dicionarioDocTermos[file] = vetorTf
    return dicionarioDocTermos

#funcao que encontra o ni, calcula a tabela IDF e retorna o vetor com os valores
def idf_table(vocabulario, dictTabelaTf):
    tfTermos = list(dictTabelaTf.values()) # lista com os arrays de tf de cada doc
    nArquivos = len(tfTermos) #tamanho da colecao de arquivos (N)
    nTermos = len(vocabulario)
    valoresNi = [0] * nTermos
    #encontra os valores ni para calcular o idf
    for i in range(nArquivos):
        for j in range(nTermos):
            if tfTermos[i][j] > 0:
                valoresNi[j] += 1
    #preenche o vetor IDF
    vetorIdf = []
    for i in range(nTermos):
        vetorIdf.append(math.log((nArquivos / valoresNi[i]), 2))
    return vetorIdf

#funcao que calcula o TF-IDF
def tfidf_table(vocabulario, dictTabelaTf, vetorIdf):
    nTermos = len(vocabulario) #tamanho do vocabulario
    dicionarioTfIdf = dict() #dicionario de valores TF-IDF
    #encontra os valores TF-IDF de cada documento e guarda em um dicionario
    for arquivo in dictTabelaTf:
        vetorTf = dictTabelaTf[arquivo]
        valoresTfIdf = []
        for i in range(nTermos):
            valoresTfIdf.append(vetorIdf[i] * vetorTf[i])
        dicionarioTfIdf[arquivo] = valoresTfIdf
    return dicionarioTfIdf

#funcao que calcula o tf da consulta
def tf_q(vocabulario, consulta):
    vetorTfDaConsulta = []
    for termo in vocabulario:
        numeroDeAparicoes = consulta.count(termo)
        if numeroDeAparicoes > 0:
            vetorTfDaConsulta.append(1.0 + math.log(numeroDeAparicoes, 2))
        else:
            vetorTfDaConsulta.append(0)
    return vetorTfDaConsulta

#funcao que calcula o tfidf da consulta
def tfidf_q(vocabulario, consulta, vetorIdfDaColecao):
    vetorTf = tf_q(vocabulario, consulta)
    vetorTfIdfDaConsulta = []
    nTermos = len(vocabulario)
    for i in range(nTermos):
        vetorTfIdfDaConsulta.append(vetorIdfDaColecao[i] * vetorTf[i])
    return vetorTfIdfDaConsulta

#funcao que normaliza os vetores dos documentos e retorna um dict com os resultados {documento : norma}
def normalize_table(dicionarioTfIdf):
    dicionarioDeNormas = dict()
    somaDosQuadrados = 0.0
    for documento in dicionarioTfIdf:
        vetorDoDocumento = dicionarioTfIdf[documento]
        for valor in vetorDoDocumento:
            somaDosQuadrados += math.pow(valor, 2)
        if somaDosQuadrados != 0.0:
            dicionarioDeNormas[documento] = math.sqrt(somaDosQuadrados)
        else:
            dicionarioDeNormas[documento] = 0.0
    return dicionarioDeNormas

#funcao que normaliza o vetor da consulta e retorna o valor da norma
def normalize_q(vetorTfIdfDaConsulta):
    normaDaConsulta = 0.0
    somaDosQuadrados = 0.0
    for valor in vetorTfIdfDaConsulta:
        somaDosQuadrados += math.pow(valor, 2)
    if somaDosQuadrados != 0.0:
        normaDaConsulta = math.sqrt(somaDosQuadrados)
    return normaDaConsulta

#funcao que calcula o numerador da fracao do score
def score_numerador(vetorTfIdfDocumento, vetorTfIdfConsulta):
    nTermos = len(vetorTfIdfDocumento)
    soma = 0.0
    for i in range(nTermos):
        soma += vetorTfIdfDocumento[i] * vetorTfIdfConsulta[i]
    return soma

#funcao que calcula o denominador da fracao do score
def score_denominador(normaConsulta, normaDocumento):
    return normaConsulta * normaDocumento

#funcao que calcula o score (modelo vetorial) e retorna o dicionario {documento : score}
def vet_score(vocabulario, consulta):
    dictTfDocumentos = tf_table(vocabulario) # <---- stemming
    vetorIdfDocumentos = idf_table(vocabulario, dictTfDocumentos)
    dictTfIdfDocumentos = tfidf_table(vocabulario, dictTfDocumentos, vetorIdfDocumentos) #encontra o TFIDF dos documentos
    dictNormaDocumentos = normalize_table(dictTfIdfDocumentos)

    vetorTfIdfConsulta = tfidf_q(vocabulario, consulta, vetorIdfDocumentos) #encontra o TFIDF da consulta
    normaConsulta = normalize_q(vetorTfIdfConsulta)

    dictEscores = dict()
    for documento in dictTfIdfDocumentos:
        dictEscores[documento] = score_numerador(dictTfIdfDocumentos[documento], vetorTfIdfConsulta) / score_denominador(normaConsulta, dictNormaDocumentos[documento])
    return dictEscores

#printa os scores em ordem decrescente
def print_score_desc(dictEscores):
    sortedEscores = dict(sorted(dictEscores.items(), key=lambda x:x[1], reverse=True))
    print("Grau de similaridade (documento : valor):")
    print(sortedEscores)


##CALCULO VETORIAL
# print da consulta pra teste
#print(consulta)
#unide(consulta)
#print(consulta)
#calculo vetorial
unide(consulta)
pre_proc(consulta, 'english')
consulta = porter_stemming(consulta)

documentoVocabulario = read_vocabulario(voc)
pre_proc(documentoVocabulario, 'english')
documentoVocabulario = porter_stemming(documentoVocabulario)
dicionarioDeEscores = vet_score(documentoVocabulario, consulta)
print_score_desc(dicionarioDeEscores)


''' CALCULO TF-IDF
vocabulario = read_vocabulario(voc)
print(vocabulario)
print('\nCalculando TF-IDF')

dicionarioTf = tf_table(vocabulario)
vetorIdf = idf_table(vocabulario, dicionarioTf)
dicionarioTfIdf = tfidf_table(vocabulario, dicionarioTf, vetorIdf)

for arquivo in glob(arquivos):
    print(arquivo + ' : ' + str(dicionarioTfIdf[arquivo]))
'''

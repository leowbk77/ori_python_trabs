'''
    Leonardo Marques Ferreira - 11921BSI235
    Script que encontra o TF-IDF da colecao billboard (n3)
    python3 n3.py
'''
from unidecode import unidecode
from glob import glob
import string
import math
import time

#caminho relativo dos arquivos .txt que serao lidos
arquivos = "top20billboard1983/*.txt"
#caminho do vocabulario a ser lido
voc = "vocbillboard.txt"

#funcao que le o arquivo e cria uma lista com as palavras
def read_file(file, wordList):
    for line in file:
        for word in line.split():
            wordList.append(word)
    file.close()

#funcao que usa o unidecode na lista para facilitar o tratamento
def unide(wordList):
    i = 0
    listSize = len(wordList)
    while i < listSize:
        wordList[i] = unidecode(wordList[i]) #unide
        wordList[i] = wordList[i].translate(str.maketrans('','', string.punctuation)) #remove a pontuacao
        wordList[i] = wordList[i].lower() #letras minusculas
        i+=1

#funcao que escreve o arquivo do vocabulario
def write_vocabulario(vocabulario):
    outputFile = open(voc, 'x')
    for word in vocabulario:
        outputFile.write(word + '\n')
    outputFile.close()

#funcao que cria o vocabulario
def create_vocabulario():
    vocabulario = []
    listaDeArquivos = glob(arquivos)
    #le os arquivos
    for file in listaDeArquivos:
        arquivo = open(file, 'rt')
        read_file(arquivo, vocabulario)
    #unidecode no vocabulario
    unide(vocabulario)
    #remove termos duplicados
    vocabulario = list(dict.fromkeys(vocabulario))
    #coloca em ordem alfabetica
    vocabulario.sort()
    #escreve o arquivo do vocabulario
    write_vocabulario(vocabulario)

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
        unide(documento)
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

def encontrar_maior_tfidf(dicionarioTfIdf, vocabulario):
    maiorValor = 0
    musicaComMaiorValor = ''
    posicaoDoTermo = 0
    for musica in dicionarioTfIdf:
        vetorTfIdf = dicionarioTfIdf[musica]
        tamanhoDoVetor = len(vetorTfIdf)
        for i in range(tamanhoDoVetor):
            if vetorTfIdf[i] > maiorValor:
                maiorValor = vetorTfIdf[i]
                musicaComMaiorValor = musica
                posicaoDoTermo = i
    print('Termo com maior TF-IDF: ' + vocabulario[posicaoDoTermo])
    print('Documento o termo: ' + musicaComMaiorValor)

ticVoc = time.perf_counter()
create_vocabulario()
tacVoc = time.perf_counter()
tempoDoVoc = tacVoc - ticVoc

vocabulario = read_vocabulario(voc)
tamanhoDoVocabulario = len(vocabulario)
print('Tempo da criacao do vocabulario: ' + str(tempoDoVoc))
print('Tamanho do vocabulario: ' + str(tamanhoDoVocabulario))
print('Calculando TF-IDF')
tic = time.perf_counter()
dicionarioTf = tf_table(vocabulario)
vetorIdf = idf_table(vocabulario, dicionarioTf)
dicionarioTfIdf = tfidf_table(vocabulario, dicionarioTf, vetorIdf)
tac = time.perf_counter()
tempoDoTfIdf = tac - tic
print('Tempo do TF-IDF: ' + str(tempoDoTfIdf))
for arquivo in glob(arquivos):
    print(arquivo + ' : ' + str(dicionarioTfIdf[arquivo]))
    print("")
encontrar_maior_tfidf(dicionarioTfIdf, vocabulario)
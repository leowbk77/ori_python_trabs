'''
    Leonardo Marques Ferreira - 11921BSI235
    Script que faz a bag of words (n2)
    python3 n2.py vocabulario.txt documento.txt
'''
import sys
from unidecode import unidecode

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
        wordList[i] = unidecode(wordList[i])
        wordList[i] = wordList[i].lower()
        i+=1

inputVocabulario = open(sys.argv[1], "rt") #vocabulario.txt
inputDocumento = open(sys.argv[2], "rt") #documento.txt

vocabulario = [] #wordlist do vocabulario
documento = [] #wordlist do documento
bagOfWords = [] #resultado final

#le os arquivos e guarda as palavras nas listas
read_file(inputVocabulario, vocabulario)
read_file(inputDocumento, documento)
unide(documento)

#verifica a existencia dos termos no documento
for termo in vocabulario:
    if documento.count(termo) == 0:
        bagOfWords.append(0)
    else:
        bagOfWords.append(1)

#escreve a saida
outputFile = open('bagofwords.txt', 'x')
for number in bagOfWords:
    outputFile.write(number + ', ')
outputFile.close()
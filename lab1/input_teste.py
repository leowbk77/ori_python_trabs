'''
    N1 funcionando quase 100% (virgula saindo)
    subir git
    fazer N2
    ------------------------------------------
    funcionalizar
'''
import sys
from unidecode import unidecode

#vars
fileName = sys.argv[1]
inputFile = open(fileName, "rt")
vocabulario = []

#teste
print(fileName + '\n')
#print(inputFile.read(5))
#teste

#le o arquivo e guarda as palavras em uma lista (vocabulario)
for line in inputFile:
    for word in line.split():
        vocabulario.append(word)

inputFile.close()

#unidecode
i = 0
vocSize = len(vocabulario)
while i < vocSize:
    vocabulario[i] = unidecode(vocabulario[i])
    vocabulario[i] = vocabulario[i].lower()
    i+=1

#remove as duplicatas do vocabulario (transformar em funcao)
vocabulario = list(dict.fromkeys(vocabulario))

#Ordem alfabetica
vocabulario.sort()

#escreve a saida
outputFile = open('output.txt', 'x')
for word in vocabulario:
    outputFile.write(word + '\n')
outputFile.close()
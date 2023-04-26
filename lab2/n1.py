'''
    Leonardo Marques Ferreira - 11921BSI235
    Script que cria o vocabulario (n1) de varios arquivos txt
    python3 n1.py
'''
from unidecode import unidecode
from glob import glob

#caminho relativo dos arquivos .txt que serao lidos
arquivos  = "txts/*.txt"

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

#funcao que escreve o arquivo do vocabulario
def write_vocabulario(vocabulario):
    outputFile = open('vocabulario.txt', 'x')
    for word in vocabulario:
        outputFile.write(word + '\n')
    outputFile.close()

#funcao que cria o vocabulario
def create_vocabulario():
    vocabulario = []
    #le os arquivos
    for file in glob(arquivos):
        read_file(file, vocabulario)
    #remove termos duplicados
    #fazer isso dentro do for pra salvar memoria?
    vocabulario = list(dict.fromkeys(vocabulario))
    #usa o unidecode (usar antes ou depois de remover os termos?)
    unide(vocabulario)
    #coloca em ordem alfabetica
    vocabulario.sort()
    #escreve o arquivo do vocabulario
    write_vocabulario(vocabulario)

#funcao que le o txt do vocabulario e retorna a lista
def read_vocabulario(path):
    vocabulario = []
    read_file(path, vocabulario)
    return vocabulario

#funcao que cria as bag of words e printa
def create_bow(vocabulario):
    #lista de termos do documento
    documento = []
    print("Bag Of Words:")
    for file in glob(arquivos):
        bagOfWords = []
        read_file(file, documento)
        for termo in vocabulario:
            if documento.count(termo) == 0:
                bagOfWords.append(0)
            else:
                bagOfWords.append(1)
        print(file + ":")
        print(*bagOfWords, sep=',')

'''
for arquivo in glob("txts/*.txt"):
    print(arquivo)
'''
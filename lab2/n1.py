'''
    Leonardo Marques Ferreira - 11921BSI235
    Script que cria o vocabulario (n1) de varios arquivos txt
    python3 n1.py
'''
from unidecode import unidecode
from glob import glob

#caminho relativo dos arquivos .txt que serao lidos
arquivos = "txts/*.txt"

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
#remover pontuacao aqui

#funcao que escreve o arquivo do vocabulario
def write_vocabulario(vocabulario):
    outputFile = open('vocabulario.txt', 'x')
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
    #remove termos duplicados
    vocabulario = list(dict.fromkeys(vocabulario))
    #unidecode no vocabulario
    unide(vocabulario)
    #coloca em ordem alfabetica
    vocabulario.sort()
    #escreve o arquivo do vocabulario
    write_vocabulario(vocabulario)

#funcao que le o txt do vocabulario e retorna a lista
def read_vocabulario(path):
    vocabulario = []
    arquivoDoVocabulario = open(path, 'rt')
    read_file(arquivoDoVocabulario, vocabulario)
    return vocabulario

#funcao que cria as bag of words e printa
def create_bow(vocabulario):
    listaDeArquivos = glob(arquivos)
    print("Bag Of Words:")
    for file in listaDeArquivos:
        bagOfWords = [] #bag of words do arquivo atual 
        documento = [] #lista de termos do arquivo atual
        arquivoAtual = open(file, 'rt') #abre o arquivo
        read_file(arquivoAtual, documento)
        unide(documento)
        for termo in vocabulario:
            if documento.count(termo) == 0:
                bagOfWords.append(0)
            else:
                bagOfWords.append(1)
        print(file + ":")
        print(*bagOfWords, sep=',')
        
for arquivo in glob("txts/*.txt"):
    print(arquivo)

print("Criando vocabulario - done")
#create_vocabulario()
print("Arquivo criado - done\nLendo o vocabulario.txt")
vocabulario = read_vocabulario("vocabulario.txt")
print(vocabulario)
print("lido. Printando bag of words")
create_bow(vocabulario)





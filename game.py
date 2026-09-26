# MARK: Desenvolvedores
# 202610383111 - Bryan Torres Ferreira
# 202610065611 - Eduardo Batista de Souza
# 202610383411 - Isaque da Silva Machado
# 202610383211 - Rodrigo dos Santos Badiali Lila

#MARK: Descrição

""""
O objetivo do jogo é formar palavras válidas a partir de uma palavra de oito letras sorteadas aleatoriamente. 
O jogador deve digitar palavras que podem ser formadas com essas letras, respeitando as regras de pontuação e validade das palavras. 
O jogo consiste em três rodadas, e o jogador pode acumular pontos com base no tamanho das palavras formadas. 
As pontuações são salvas em um arquivo para referência futura.
"""

# MARK: Bibliotecas
import os
import random
from collections import Counter
from spellchecker import SpellChecker

#MARK: Variaveis
titulo= 'ANAGRAMA'
tituloRegras= 'REGRAS'
regras = 'Será dada pra você uma palavra que contém oito letras. Seu objetivo é formar palavras' '\n' \
'existentes com elas(O mínimo de letras para uma palavra são três).' '\n' \
'De acordo com o número de letras da palavra, poderá pontuar da seguinte forma:' '\n' \
'Entre 3 e 4 letras: 3 pontos' '\n' \
'Entre 5 e 7 letras: 6 pontos' '\n' \
'8 letras: 10 pontos' '\n' \
'Se você digitar uma palavra impossível para a sequência ou repetir palavras, não pontuará,''\n' \
'O jogo será composto por 3 rodadas.' '\n' \
'Pontue o máximo que puder, boa sorte!'

# Carrega o motor de verificação de ortografía para verificar se a palavra digitada pelo jogador é valida.
checker = SpellChecker(language='pt')

# Armazena as pontuaações dos jogadores, obtidas a partir do arquivo "pontuacoes.txt", e as atualiza de acordo com jogo.
pontuacoes = {}

#Descreve a quantidade de letras que será fornecida ao usuário para formar palavras
qntdLetras = 8

#Descreve o minimo de letras que uma palavra deve ter para ser considerada válida
minLetras = 3

#MARK: Funções

#Exibe o titulo centralizado, as regras do jogo e solicita o nome do jogador
def welcome():
    print(titulo.center(40))
    print(tituloRegras.center(40))
    print(regras)

# Atualiza o dicionario de pontuações, adicionando um jogador na lista ou atualizando a pontuação de algum jogador ja existente
def adicionarPontuacao(nome, pontuacao):
    if nome in pontuacoes:
        pontuacoes[nome] += pontuacao
    else:
        pontuacoes[nome] = pontuacao

# Procura o arquivo pontuações e carrega as pontuações existentes, ou cria um novo arquivo se não existir
def carregarPontuacoes():
    if os.path.exists("pontuacoes.txt"):
        # Carrega as pontuações do arquivo "pontuacoes.txt"
        with open("pontuacoes.txt", "r", encoding="utf-8") as f:
            for line in f:
                nome, pontuacao = line.strip().split(',')
                pontuacoes[nome] = int(pontuacao)
    else:
        # Se o arquivo não existir, cria um novo
        with open("pontuacoes.txt", "w", encoding="utf-8") as f:
            pass

# Após o fim de uma rodada, salva as pontuações atualizadas no arquivo "pontuacoes.txt"
def salvarPontuacoes():
    with open("pontuacoes.txt", "w", encoding="utf-8") as f:
        for name, score in pontuacoes.items():
            f.write(f"{name},{score}\n")

# Com base na quantidade de letras da palavra digitada pelo usuário, calcula a pontuação que será atribuida para aquela tentativa.
def calcular_pontos(palavra):
    mensagem = f">> A palavra '{palavra}' é válida e você ganhou "
    tamanho = len(palavra)
    if 3 <= tamanho <= 4:
        print(mensagem + "3 pontos.\n")
        return 3
    elif 5 <= tamanho <= 7:
        print(mensagem + "6 pontos.\n")
        return 6
    elif tamanho == 8:
        print(mensagem + "10 pontos.\n")
        return 10
    else:
        print(f">> A palavra '{palavra}' não é válida para pontuação.\n")
        return 0

# Ordena as pontuações em ordem decrescente e exibe para o jogador a lista de pontuações
def ordernarEExibirPontuacoes():
    # Ordena as pontuações em ordem decrescente
    pontuacoes_sorteadas = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    if len(pontuacoes_sorteadas) > 0:
        print("Pontuações:")
        for name, score in pontuacoes_sorteadas:
            print(f"{name}: {score}")
    else:
        print("Nenhuma pontuação registrada.")

# Sorteia uma palavra aleatória, no arquivo "palavras.txt", que tenha 8 letras.
def sortear_palavra() -> str:
    with open("palavras.txt", "r", encoding="utf-8") as f:
        palavras = [line.strip() for line in f if len(line.strip()) == qntdLetras]
    return random.choice(palavras) if palavras else ""

# Verifica se a palavra ja foi utilizada anteriormente pelo jogador.
def jaUsada(palavra, palavras_usadas) -> bool:
    if palavra in palavras_usadas:
        print(">> Você já usou essa palavra.\n")
        return True

    return False

# Verifica se a palavra digitada pelo jogador possui pelo menos 3 letras.
def eMaiorQueTres(palavra) -> bool:
    if len(palavra) < minLetras:
        print(f">> A palavra precisa ter pelo menos {minLetras} letras.\n")
        return False

    return True

# Verifica se a palavra digitada pelo jogador é possível de ser formada com a sequência de letras fornecida.
def palavra_formavel(palavra, palavrasDigitadas) -> bool:
    contagem_disponivel = Counter(palavrasDigitadas)
    contagem_palavra = Counter(palavra)

    for letra, qtd in contagem_palavra.items():
        if contagem_disponivel.get(letra, 0) < qtd:
            print(">> Essa palavra não pode ser formada com as letras sorteadas.\n")
            return False
    return True

# Verifica se a palavra digitada pelo jogador é uma palavra válida, ou seja, se ela existe no dicionário da lingua portuguesa.
def eReal(palavra: str) -> bool:
    unknownWord = list(checker.unknown([palavra])) # Verifica se a palavra é candidata a uma palavra desconhecida e converte de set para lista
    if len(unknownWord) == 1: # Se a lista estiver vazia, significa que a palavra é válida
        print(">> Essa palavra não existe na língua portuguesa.\n")
        return False
    return True

# Verifica se a palavra digitada pelo jogador é igual a palavra base sorteada.
def igual(palavra, palavra_base) -> bool:
    if palavra == palavra_base:
        print(">> Você já usou essa palavra.\n")
        return True
    return False

# Verifica se a palavra digitada pelo jogador é válida, ou seja, se ela atende a todos os critérios de validação.
def rodadaValida(palavra, palavra_base, palavras_usadas) -> bool:
    if igual(palavra, palavra_base):
        return False

    if jaUsada(palavra, palavras_usadas):
        return False

    if not eMaiorQueTres(palavra):
        return False

    if not palavra_formavel(palavra, palavra_base):
        return False

    if not eReal(palavra):
        return False

    return True

# Responsável por gerenciar a execução do jogo como um todo.
def jogar():
    welcome()
    carregarPontuacoes()
    ordernarEExibirPontuacoes()
    nome = input("Digite seu nome: ")
    rodadas = 3
    palavras_usadas = set()
    palavra_base = sortear_palavra()
    print("Palavra sorteadas:", palavra_base.upper())

    while rodadas > 0:
        palavra = input("Digite uma palavra: ").strip().lower()

        if palavra == "":
            print(">> Entrada vazia. Por favor, digite uma palavra.\n")
            continue
        elif palavra == "sair":
            print(">> Saindo do jogo.\n")
            break

        if rodadaValida(palavra, palavra_base, palavras_usadas):
            adicionarPontuacao(nome, calcular_pontos(palavra))
        else:
            print(f">> A palavra '{palavra}' não é válida.\n")

        # Se a palavra passou por todas as verificações, ela é válida
        palavras_usadas.add(palavra)
        rodadas -= 1
        print(f"Rodadas restantes: {rodadas}\n")

    print(f"Fim do jogo! Sua pontuação final é: {pontuacoes[nome]}")

#MARK: Loop principal do jogo
#loop principal que mantém o jogo funcionando, enquanto não for encerrado
gameIsRunning=True 
while gameIsRunning:
    jogar()
    salvarPontuacoes()
    ordernarEExibirPontuacoes()
    continuar = input("Deseja jogar novamente? (s/n): ").strip().lower()
    if continuar != 's':
        gameIsRunning = False
        print("Obrigado por jogar!")
########################################################################
# Fatec Antonio Russo - JOGNA5 - Tecnologia de Redes de Computadores   #
# Nome do Jogo: Jogo da Velha - Interface Servidor                     #
# Componentes do Grupo:                                                #
#        Bruno Pedreira Gonçalves                                      #
#        Carlos Antonio dos Reis                                       #
#        Gustavo Tajima Moraes                                         #
#        Thiago Oliveira Monte Alves de Araujo                         #
########################################################################

""" Importação das Bibliotecas - Pygame """

import sys, math, json
from random import randint
from socket import *

# Configuração de Comunicação
serverPort = 1200                                            # Porta
serverSocket = socket(AF_INET,SOCK_STREAM)                   # Socket 
serverSocket.bind(("",serverPort))
serverSocket.listen(5)                                       # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) 
                                                             # antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

# Dados do Jogo
DadosJogo = []
Flag_JogaServer = False;

########################################################################
#        Informa na Coluna Resultado as Células Ganhadoras             #
########################################################################

def registra_resultado( Trinca, LinCol ):

  global DadosJogo

  if Trinca == 'L':
    j = 0
    while j <= 2:    
      for posicao in DadosJogo:  
        if ( posicao[0][0] == LinCol ) and ( posicao[0][1] == j ):
          posicao[7] = posicao[6]
      j = j + 1
  elif Trinca == 'C':
    j = 0
    while j <= 2:    
      for posicao in DadosJogo:  
        if ( posicao[0][0] == j ) and ( posicao[0][1] == LinCol ):
          posicao[7] = posicao[6]
      j = j + 1
  elif Trinca == 'DP':
    j = 0
    while j <= 2:    
      for posicao in DadosJogo:  
        if ( posicao[0][0] == j ) and ( posicao[0][1] == j ):
          posicao[7] = posicao[6]
      j = j + 1
  elif Trinca == 'DI':
    j = 0
    k = 2
    while j <= 2:    
      for posicao in DadosJogo:  
        if ( posicao[0][0] == k-j ) and ( posicao[0][1] == j ):
          posicao[7] = posicao[6]
      j = j + 1

  Flag_JogaServer = False

########################################################################
#              O servidor faz a Jogada do Oponente                     #
########################################################################
def server_faz_jogada():

  global DadosJogo

  ContaJogada = 0
  
  for posicao in DadosJogo:
    if (posicao[6] != '*'):
      ContaJogada += 1
  if ContaJogada < 9:
    Flag_Jogada = True
    while Flag_Jogada:
      i = randint(0, 2)
      j = randint(0, 2)
      for posicao in DadosJogo:
        if ( posicao[0][0] == i ) and ( posicao[0][1] == j ) and ( posicao[6] == '*' ):
          if posicao[5] == 'X':      
            posicao[6] = 'O'
          else:
            posicao[6] = 'X'
          Flag_Jogada = False
        
########################################################################
#        Verifica o Resultado da Jogada Recebida/Efetuada              #
########################################################################
def exec_verifica_jogada():

  global DadosJogo

  Flag_Resultado = True

  # Verifica Resultados nas Linhas
  LinCol = 0
  while LinCol <= 2:
    LC1 = '#'
    LC2 = '#'
    LC3 = '#'
    for posicao in DadosJogo:  
      if ( posicao[0][0] == LinCol ) and ( posicao[0][1] == 0 ):
        LC1 = posicao[6]
      elif ( posicao[0][0] == LinCol ) and ( posicao[0][1] == 1 ):
        LC2 = posicao[6]
      elif ( posicao[0][0] == LinCol ) and ( posicao[0][1] == 2 ):
        LC3 = posicao[6]
      if (LC1 != '#') and (LC2 != '#') and (LC3 != '#'):
        if (LC1 == LC2) and (LC2 == LC3):
          Flag_Resultado = False           
          registra_resultado( 'L', LinCol )
          break;
    LinCol += 1    

  # Verifica Resultados nas Colunas
  if Flag_Resultado:
    LinCol = 0
    while LinCol <= 2:
      LC1 = '#'
      LC2 = '#'
      LC3 = '#'
      for posicao in DadosJogo:  
        if ( posicao[0][0] == 0 ) and ( posicao[0][1] == LinCol ):
          LC1 = posicao[6]
        elif ( posicao[0][0] == 1 ) and ( posicao[0][1] == LinCol ):
          LC2 = posicao[6]
        elif ( posicao[0][0] == 2 ) and ( posicao[0][1] == LinCol ):
          LC3 = posicao[6]
        if (LC1 != '#') and (LC2 != '#') and (LC3 != '#'):
          if (LC1 == LC2) and (LC2 == LC3):
            Flag_Resultado = False           
            registra_resultado( 'C', LinCol )
            break;
      LinCol += 1    

  # Verifica Resultados Diagonal Principal "DP"
  if Flag_Resultado:
    LC1 = '#'
    LC2 = '#'
    LC3 = '#'
    for posicao in DadosJogo:  
      if ( posicao[0][0] == 0 ) and ( posicao[0][1] == 0 ):
        LC1 = posicao[6]
      elif ( posicao[0][0] == 1 ) and ( posicao[0][1] == 1 ):
        LC2 = posicao[6]
      elif ( posicao[0][0] == 2 ) and ( posicao[0][1] == 2 ):
        LC3 = posicao[6]
      if (LC1 != '#') and (LC2 != '#') and (LC3 != '#'):
        if (LC1 == LC2) and (LC2 == LC3):
          Flag_Resultado = False           
          registra_resultado( 'DP', 0 )
          break;

  # Verifica Resultados Diagonal Invertida "DI"
  if Flag_Resultado:
    LC1 = '#'
    LC2 = '#'
    LC3 = '#'
 
    for posicao in DadosJogo:  
      if ( posicao[0][0] == 2 ) and ( posicao[0][1] == 0 ):
        LC1 = posicao[6]
      elif ( posicao[0][0] == 1 ) and ( posicao[0][1] == 1 ):
        LC2 = posicao[6]
      elif ( posicao[0][0] == 0 ) and ( posicao[0][1] == 2 ):
        LC3 = posicao[6]
      if (LC1 != '#') and (LC2 != '#') and (LC3 != '#'):
        if (LC1 == LC2) and (LC2 == LC3):
          Flag_Resultado = False           
          registra_resultado( 'DI', 2 )
          break;

    
########################################################################
#        PROGRAMA PRINCIPAL - VERSÃO PARA O JOGADOR                    #
########################################################################

# Formatação JSON para o envio de Dados

DataStrJson = ''

while True:

  connectionSocket, addr = serverSocket.accept()  
  sentence = connectionSocket.recv(65000)
  DataStrJson = str(sentence,"utf-8")

  # print( "Dados Recebidos \n \n" + DataStrJson)
  print( "\n Dados Recebidos \n")
  
  DadosJogo = json.loads(DataStrJson) 

  Flag_JogaServer == False
  
  exec_verifica_jogada()

  if Flag_JogaServer != True:
    server_faz_jogada()
    exec_verifica_jogada()
    
  DataJsonStr = json.dumps(DadosJogo)

  # print( "Dados Transmitidos \n \n" + DataJsonStr)
  print( "\n Dados Transmitidos \n")
    
  connectionSocket.send(bytes(DataJsonStr, "utf-8"))
  connectionSocket.close()


  


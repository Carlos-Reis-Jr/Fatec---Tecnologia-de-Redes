########################################################################
# Fatec Antonio Russo - JOGNA5 - Tecnologia de Redes de Computadores   #
# Nome do Jogo: Jogo da Velha - Interface Cliente                      #
# Componentes do Grupo:                                                #
#        Bruno Pedreira Gonçalves                                      #
#        Carlos Antonio dos Reis                                       #
#        Gustavo Tajima Moraes                                         #
#        Thiago Oliveira Monte Alves de Araujo                         #
########################################################################

""" Importação das Bibliotecas - Pygame """

import pygame, sys, math, json
from pygame.locals import *
from random import randint, shuffle
from socket import *

# Configuração de Comunicação
serverName = "127.0.0.1"                                     # IP do Servidor (Default Localhost)
serverPort = 1200                                            # Porta
clientSocket = socket(AF_INET, SOCK_STREAM)                  # Socket 

# Definição de Variaveis para Telas / Cores / Dimensões 
CorPainel = (128, 203, 196)                                  # Cinza
CorFundo  = (187, 222, 251)                                  # Branco
CorBorda  = (38, 166, 154)                                   # Cor da Borda
CorPeca   = (244, 16, 0)                                     # Cor da Peça
CorTrinca = (204, 255, 255)                                  # Cor das Peças qdo Formam a Trinca
ObjPc     = []                                               # Peças do Tabuleiro [ ( x, y, z ), 'Valor' ]

# Cores para Textos
CorTitulo  = (255, 214, 0)                                   # Amarelo
CorMensag  = (245, 127, 23)                                  # Laranja
CorBarra   = (255, 87, 34)                                   # Vermelho
CorFillBox = (51, 153, 102)                                  # Verde

# Dimensões do Painel e Borda
PnLarg    = 1024                                             # Largura do Painel
PnAlt     = 576                                              # Altura do Painel
PsizeT    = 400                                              # Tamanho do Tabuleiro do Jogo
EspBorda  = 3                                                # Espessura da Borda
MatrizOrd = 3                                                # Quantidade de Linhas Colunas da Matriz
CoordArea = [0,0,PnLarg,PnAlt]                               # Area Total
TamImgNor = [16,16]                                          # Tam. em pixels das Imagens Normais
TamImgAtv = [16,16]                                          # Tam. em pixels das Imagens Ativas
PassoNorm = 0.25                                             # Passo da Imagem Normal
PassoAtv  = 0.25                                             # Passo da Imagem Ativa

########################################################################
#                    Geração das Peças do Tabuleiro                    #
########################################################################

def load_array_pecas(Tipo):

  global ObjPc, PsizeT, PnLarg, PnAlt, MatrizOrd, CorFillBox, CorBarra, EspBorda, CorPeca

  # Inicializa o Array de Peças
  ObjPc.clear()
  # Total de Pixels por célula/Divisão do Tabuleiro
  Prazao = (PsizeT - (EspBorda *(MatrizOrd -1))) // MatrizOrd
  # Coordenadas do Canto Superior Esquerdo
  PsupX = ((PnLarg - PsizeT) // 2) 
  PsupY = ((PnAlt - PsizeT) // 2) 

  # Carga Inicial para o Jogo
  i = 0
  while i <= (MatrizOrd-1):
    j = 0
    while j <= (MatrizOrd-1):
      PosXi = PsupX + (EspBorda // 2) + (EspBorda * i) + (Prazao * i)    # X Superior Esquerdo
      PosYi = PsupY + (EspBorda // 2) + (EspBorda * j) + (Prazao * j)    # Y Superior Esquerdo
      PosXf = PosXi + Prazao - EspBorda                                  # X Inferior Direito
      PosYf = PosYi + Prazao - EspBorda                                  # Y Inferior Direito
      PtamL = Prazao-EspBorda                                            # Tamanho do Lado
      PmedX = (PosXf + PosXi) // 2                                       # X Ponto Médio
      PmedY = (PosYf + PosYi) // 2                                       # Y Ponto Médio
      RaioC = ((PosXf - PosXi) // 2) - 3                                 # Raio Bolinha
      ObjPc.append( [(i,j),(PosXi,PosYi,PosXf,PosYf),(PmedX,PmedY),PtamL,RaioC,Tipo,'*','*'] )
      j += 1
    i += 1

########################################################################
#                    Desenho do Tabuleiro                              #
#   (Grade, Mensagens, Fundo da Área Jogável, Posições Preenchidas )   #
########################################################################

def draw_noughts_crosses():  

  global ObjPc, Flag_Resultado, CorFillBox, CorBarra, EspBorda, CorPeca, CorTrinca

  Flag_Vitoria  = False
  Flag_Derrota  = False
  Total_Marcado = 0
  Msg_Resultado = ''

  for n in range(len(ObjPc)):
    PosXi = ObjPc[n][1][0] 
    PosYi = ObjPc[n][1][1]
    PosXf = ObjPc[n][1][2]
    PosYf = ObjPc[n][1][3]
    PtamL = ObjPc[n][3]
    PmedX = ObjPc[n][2][0]
    PmedY = ObjPc[n][2][1]
    RaioC = ObjPc[n][4]
    EspeX = 20
    CorJogada = CorPeca

    pygame.draw.rect(painel, CorFillBox, (PosXi,PosYi,PtamL,PtamL), 0)

    if ObjPc[n][7] != '*':
      # Vitoria
      if ObjPc[n][5] == ObjPc[n][7]:
        Flag_Vitoria = True
        Msg_Resultado = 'Você Ganhou !!! '
      # Derrota
      if ObjPc[n][5] != ObjPc[n][7]:
        Flag_Derrota = True
        Msg_Resultado = 'Você Perdeu.'
      CorJogada = CorTrinca
    if ObjPc[n][6] == 'X':
       # Desenho das Marcações X
       pygame.draw.line(painel, CorJogada, (PosXi + EspeX, PosYi + EspeX), (PosXf - EspeX, PosYf - EspeX), EspeX)
       pygame.draw.line(painel, CorJogada, (PosXi + PtamL - EspeX, PosYi + EspeX), (PosXf - PtamL + EspeX, PosYf- EspeX), EspeX)
    elif ObjPc[n][6] == 'O':
      # Desenho das Marcações O
      pygame.draw.circle(painel, CorJogada, (PmedX, PmedY), RaioC, 0)
      pygame.draw.circle(painel, CorFillBox, (PmedX, PmedY), RaioC - EspeX, 0)

    # Total de Células com Marcações
    if ObjPc[n][6] != '*':
      Total_Marcado += 1

  # Verifica se há Resultado (Vitoria, Derrota ou Empate)
  if (Flag_Vitoria == True) or (Flag_Derrota == True) or (Total_Marcado == 9):
    Flag_Resultado = True
    if (Flag_Vitoria != True) and (Flag_Derrota != True):
      Msg_Resultado = 'Empate'
    draw_text_message('>>> '+ Msg_Resultado + ' <<<', 54, CorMensag, CorPainel, PercentX=50, PercentY=10 )
    draw_text_message('Tecle [Espaço] para Jogar Novamente ou [Esc] para o Início', 28, CorMensag, CorPainel, PercentX=50, PercentY=90 )
  pygame.display.update()

########################################################################
#             Desenho da Grade com Instruções ao Redor                 #
########################################################################

def draw_grade_jogo(Tipo):

  global ObjPc, PsizeT, PnLarg, PnAlt, MatrizOrd, CorBorda, CorBarra, EspBorda, CorPeca

  # Limpa Painel 
  draw_backg_screen()

  # Mensagens no Topo e Abaixo
  draw_text_message('Voce está jogando com [' + Tipo + ']', 32, CorMensag, CorPainel, PercentX=50, PercentY=10 )
  draw_text_message('Clique na área de Jogo. [ESC] Abandona.', 32, CorMensag, CorPainel, PercentX=50, PercentY=90 )

  # Frame do Tabuleiro
  Pos_Xi = ((PnLarg - PsizeT) // 2) - EspBorda
  Pos_Yi = ((PnAlt - PsizeT) // 2) - EspBorda
  Pos_Xf = PsizeT + EspBorda
  Pos_Yf = PsizeT + EspBorda
  pygame.draw.rect(painel, CorBarra, (Pos_Xi, Pos_Yi, Pos_Xf, Pos_Yf), EspBorda)
  
  # Divisões - Verticais e Horizontais
  Prazao = ((PsizeT - (2 * EspBorda)) // MatrizOrd)
  i = 1
  while i <= (MatrizOrd -1):
    Pln_Xi = ((PnLarg - PsizeT) // 2) + (Prazao * i) + (EspBorda * (i-1))
    Pln_Yi = ((PnAlt - PsizeT) // 2) 
    Pln_Xf = Pln_Xi
    Pln_Yf = Pln_Yi + PsizeT - EspBorda
    pygame.draw.line(painel, CorBarra, (Pln_Xi, Pln_Yi), (Pln_Xf, Pln_Yf), EspBorda)
    Pln_Xi = ((PnLarg - PsizeT) // 2) #312 + 126 = 438
    Pln_Yi = ((PnAlt - PsizeT) // 2)  + (Prazao * i) + (EspBorda * (i-1))
    Pln_Xf = Pln_Xi  + PsizeT - EspBorda
    Pln_Yf = Pln_Yi
    pygame.draw.line(painel, CorBarra, (Pln_Xi, Pln_Yi), (Pln_Xf, Pln_Yf), EspBorda)
    i += 1
  pygame.display.update()

########################################################################
#             Gera a Imagem da Mensagem e Exibe na Tela                #
########################################################################
      
def draw_text_message(Pmsg, Psize=32, Pcor=CorMensag, Pfundo=CorPainel, PercentX=0, PercentY=0, Pfonte='freesansbold.ttf' ):

  global PnLarg, PnAlt
  
  if len(Pmsg) > 0:
    if PercentX == 0:
      PosX = PnLarg // 2
    else:
      PosX = math.trunc( PnLarg * (PercentX / 100))
    if PercentY == 0:
      PosY = PnAlt // 2
    else:
      PosY = math.trunc( PnAlt * (PercentY / 100))
    fonte_texto       = pygame.font.Font(Pfonte, Psize)
    texto_exibido     = fonte_texto.render(Pmsg, True, Pcor, Pfundo)
    area_texto        = texto_exibido.get_rect()
    area_texto.center = (PosX, PosY)
    painel.blit(texto_exibido, area_texto)
    pygame.display.update()

########################################################################
#        Desenha a Tela de Abertura/Principal com as Opções            #
########################################################################

def draw_menu_screen():

  # Desenha a Tela Inicial de Menu com a Opção de Escolha do Tipo de Peça para Inicio do Jogo

  # Título
  draw_text_message('Jogo da Velha', Psize=72, Pcor=CorTitulo, Pfundo=CorPainel, PercentX=0, PercentY=20 )
    
  # Mensagem Tela Principal
  draw_text_message('Tecle [X] ou [O] para jogar', Psize=44, Pcor=CorMensag, Pfundo=CorPainel, PercentX=0, PercentY=80 )

########################################################################
#        Preenche a Tela com a Cor de Fundo (Limpa a Tela)             #
########################################################################

def draw_backg_screen():
  pygame.draw.rect(painel, (CorPainel), (CoordArea), 0)
  painel.fill((CorPainel))
  pygame.display.update()

########################################################################
#     Envio/Recepção (Marcações Jogador X Server) e Resultado          #
########################################################################
  
def play_server_connect():

  global ObjPc, Loop_Jogo, Flag_Resultado

  # Formatação JSON para o envio de Dados

  DataJsonC = json.dumps(ObjPc)                             

  # Envio e Recepção das Informações Processadas no Server
  clientSocket = socket(AF_INET, SOCK_STREAM)               
  clientSocket.connect((serverName,serverPort))
  clientSocket.send(bytes(DataJsonC, "utf-8"))
  DataJsonS = clientSocket.recv(65000)
  clientSocket.close()

  # Carrega as Informações devolvidas pelo Servidor
  MatrizT = json.loads(DataJsonS)

  # Atualiza ObjPc com as novas Marcações
  for p in range(len(MatrizT)):
    for n in range(len(ObjPc)):
      if MatrizT[p][0][0] == ObjPc[n][0][0] and MatrizT[p][0][1] == ObjPc[n][0][1]:
        ObjPc[n][6] =  MatrizT[p][6]
        ObjPc[n][7] =  MatrizT[p][7]
  MatrizT.clear()
          

########################################################################
#        Preenche a Tela com a Cor de Fundo (Limpa a Tela)             #
########################################################################

def play_noughts_crosses(Tipo):

  global ObjPc, Flag_Resultado, Loop_Jogo, serverName, serverPort, clientSocket

  load_array_pecas (Tipo)
  draw_grade_jogo(Tipo)

  while Loop_Jogo:

    draw_noughts_crosses()

    Flag_Jogo = False
    
    for event in pygame.event.get():

      Flag_Jogo = False
    
      if event.type == QUIT:
        Loop_Jogo = False
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          Loop_Jogo = False
        elif event.key == K_SPACE:
          Loop_Jogo = True
          Flag_Resultado = False
          load_array_pecas (Tipo)
          draw_grade_jogo(Tipo)
      elif event.type == MOUSEBUTTONDOWN:
        if Flag_Resultado != True:
          mouseX, mouseY = event.pos
          # Verifica se Pressionou o Mouse na área de Jogo
          for n in range(len(ObjPc)):
            Pxi = ObjPc[n][1][0]
            Pxf = ObjPc[n][1][2]
            Pyi = ObjPc[n][1][1]
            Pyf = ObjPc[n][1][3]
            if ( ( mouseX >= Pxi and mouseX <= Pxf ) and ( mouseY >= Pyi and mouseY <= Pyf ) ):
              if ObjPc[n][6] == '*':
                ObjPc[n][6] = ObjPc[n][5]
                Flag_Jogo = True
                continue;
    if Flag_Jogo:
      draw_grade_jogo(ObjPc[n][5])
      draw_noughts_crosses()
      play_server_connect()

########################################################################
#        PROGRAMA PRINCIPAL - VERSÃO PARA O JOGADOR                    #
########################################################################

# Controle de Loop
Loop_Programa = True                                         # Controla o LOOP do Jogo
Loop_Jogo     = False                                        # Controla o LOOP da Partida

# Inicialização do PyGame
pygame.init() 
painel = pygame.display.set_mode((PnLarg,PnAlt), 0, 32) 
pygame.display.set_caption('Jogo da Velha')

# Programa Principal
draw_backg_screen()
draw_menu_screen()
  
while Loop_Programa:

  for event in pygame.event.get():
    
    #Detecção de Encerramento
    
    if event.type == QUIT:
      Loop_Programa = False
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        draw_backg_screen()
        draw_menu_screen()
        continue;
      elif event.key == K_x:
        Loop_Jogo = True
        Flag_Resultado = False
        play_noughts_crosses('X')
      elif event.key == K_o:
        Loop_Jogo = True
        Flag_Resultado = False
        play_noughts_crosses('O')
  
pygame.quit()
quit()
 

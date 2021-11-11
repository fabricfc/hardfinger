#!-*- coding: utf8 -*

profileList = [
      [ #00 - Test
         [[],[],['myemail@nti.ifes.br']], #MailTO | MailCC | MailCCO
         200, # Threshold do tamanho do arquivo
         [False, 1], # Checagem de data de arquivo e limite de tempo em dias 
         'suspectwords.txt', # Caminho do arquivo que contém palavras chaves 
         ['/opt/home/setores/PROGEP/','\\TESTE\\', 'test'], #Local a ser vasculhado | Nome de perfil que irá aparecer | nome do perfil
         "(Mensagem automática) Foram encontrados alguns arquivos que merecem atenção" # Assunto do email
      ],
      [ #01 - ASCOM
         [['direcao@ascom.ifes.br'],[],['myemail@nti.ifes.br', 'diretor@nti.ifes.br']], 
         200, 
         [False, 1],  
         'suspectwords_ascom.txt',  
         ['/opt/home/setores/ASCOM/','\\ASCOM\\', 'ascom'], 
         "(Mensagem automática) Foram encontrados alguns arquivos que merecem atenção" 
      ],
      [ #02 - DAP
         [['direcao@dap.ifes.br'],[],['myemail@nti.ifes.br', 'diretor@nti.ifes.br']], 
         200, 
         [False, 1],  
         'suspectwords.txt',  
         ['/opt/home/setores/DAP/','\\DAP\\', 'dap'], 
         "(Mensagem automática) Foram encontrados alguns arquivos que merecem atenção" 
      ]
   ]

# Lista de emails do dono
# print ownerList[0][0][0]

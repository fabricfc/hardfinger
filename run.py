#!-*- coding: utf8 -*
import sys
from list import profileList
import settings
from searchengine.searchengine_probabilistic import searchEngine

def run (profile, settings):
   rootSetor = profile[4][0]   
   rootShow = profile[4][1]
   suspectNamesFile = profile[3]
   dateValidation = profile[2][0]
   dateTimeSpanValidation = profile[2][1]
   maxFileSize = profile[1]   
   escala = settings.escalaMB
   subject = profile[5]
   rootOwnerMail = profile[0][0]
   rootCCMail = profile[0][1]
   rootBCCMail = profile[0][2]
   isDebug = settings.isDebug

   searchEngine(settings, rootSetor, rootShow, 
            suspectNamesFile, dateValidation, dateTimeSpanValidation, maxFileSize, 
            escala, 
            subject, rootOwnerMail, rootCCMail, rootBCCMail, settings.replyToMail,
            isDebug)

if len(sys.argv) <= 1:
   print("Este aplicativo precisa de uma argumento que \nfaz referencia um index/nome de perfil no arquivo list.py.\n\nEx: python run.py 3 <- (Refer�ncia ao terceiro indice no arquivos)")
   quit()

indice = -1
try:
   indice = int(sys.argv[1])
except:
   counter = 0
   for setor in profileList:      
      if str(setor[4][2]).lower() == sys.argv[1]:
         indice = counter 
      counter = counter + 1
if indice < 0:
   print("Perfil de execução inexistente")
   quit()
else:
   if indice > len(profileList)-1:
      print("Índice de perfil de execução inexistente")
   else:
      run (profileList[indice], settings)
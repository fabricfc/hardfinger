#!-*- coding: utf8 -*
import os
import operator

from datetime import datetime
# File tasks
from readfile import getList, modification_date
# Mail tasks
from sendmail import sendEmail
#    import sendEmail
import probabilistic  

def searchEngine(settings, rootSetor, rootShow, 
                 suspectNamesFile, dateValidation, dateTimeSpanValidation, maxFileSize, 
                 escala, 
                 subject, rootOwnerMail, rootCCMail, rootBCCMail, replytoAddrs, 
                 isDebug):
   suspectWords = getList(suspectNamesFile)
   
   fileSizeAverage = 0
   fileSizeTotal = 0
   fileCount = 0
   filesReportName = dict()
   filesReportSize = dict()
   filesSuspectNumber = dict()
   
   for (root, dirnames, filenames) in os.walk(rootSetor):   
      for filename in filenames:
         fileuri = os.path.join(root, filename)
         # Para exibição no email
         fileShow = fileuri.replace(rootSetor, rootShow).replace("/", settings.separador)      
         try:
            filesize = os.path.getsize(fileuri)        
            fileCount = fileCount + 1        
            fileSizeTotal = fileSizeTotal + filesize            
         except:
            continue
         
         dateFlag = True
         
         if (dateValidation):
            datetimeSpan = datetime.now() - modification_date(fileuri)
            if (datetimeSpan.days >= dateTimeSpanValidation): # Checando se tem mais de 24
               dateFlag = False
   
         if (dateFlag):
            if (filesize >= maxFileSize*escala):
               filesReportSize[fileShow] = filesize
            
            suspectCounter = 0
            for suspectword in suspectWords:
               if (suspectword.upper() in filename.upper()):
                  filesReportName[fileShow] = filesize
                  suspectCounter = suspectCounter + 1
            if (suspectCounter > 1):
               filesSuspectNumber[fileShow] = suspectCounter
                  
   if (fileCount > 0):
      fileSizeAverage = float(fileSizeTotal)/float(fileCount)
      
      fileProblems = ("Prezado Gestor,\n\n" + 
                      "\t Visando uma melhor utilização do espaço da pasta do setor (no servidor de arquivos), " + 
                      "trouxemos uma lista com o tamanho e o nome dos arquivos que podem causar " +
                      "falta de espaço e alguns problemas legais (que podem estar violando a política de utilização). \n\n" + 
                      "\t Assim, sugerimos que veja cautelosamente se os arquivos devem permanecer na pasta do setor e solicite, " + 
                      "caso necessário, a remoção do arquivo à pessoa que o colocou." +
                      "\n\n" +
                      "Atenciosamente, \n Equipe de Redes do NTI" +
                      "\n\n") + ("Tamanho médio: %0.2f MB | (Total de arquivos: %d) | (Uso de disco: %0.2f MB) \n" % 
              (fileSizeAverage/(escala), fileCount, fileSizeTotal/(escala)))
      
      sendMailFlag = False
      if len(filesReportSize) > 0:
         #Sorting by size
         filesReportSize = sorted(filesReportSize.items(), key=operator.itemgetter(1), reverse=True)
         fileProblems = (fileProblems + 
                         ("%sArquivos com tamanhos suspeitos (Acima de %d MB):%s" % 
                          (settings.lineBreaker, maxFileSize, settings.lineBreaker)))
         for key in filesReportSize:    
            fileProblems =  fileProblems + '%5.2f MB | ' %  float(float(key[1])/(escala)) + key [0]+ "\n"
         sendMailFlag = True
      
      if len(filesReportName) > 0:
         #Sorting by Name
         filesReportName = sorted(filesReportName.items(), key=operator.itemgetter(1), reverse=True)
         fileProblems = (fileProblems + 
                         "%sArquivos com nomes suspeitos:%s" % 
                         (settings.lineBreaker, settings.lineBreaker))
         for key in filesReportName:
            fileProblems =  fileProblems + ('%5.2f MB | ' %  float(float(key[1])/(escala)) + key[0]) + "\n"
         sendMailFlag = True 
      
      if sendMailFlag:
         sendEmail (settings.systemMail, 
            rootOwnerMail, rootCCMail, rootBCCMail, settings.replyToMail, 
            subject, fileProblems, 
            settings.systemMail, settings.systemPasswd, settings.smtpServer, settings.smtpPort, isDebug)
   else:
      print "Pasta \"%s\" não encontrada! " % rootSetor

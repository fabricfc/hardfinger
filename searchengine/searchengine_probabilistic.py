#!-*- coding: utf8 -*
import os
import operator

from datetime import datetime
# File tasks
from readfile import getList, modification_date
# Mail tasks
from sendmail import sendEmail
#    import sendEmail
from probabilistic import suspectFileProbability  

def searchEngine(settings, rootSetor, rootShow, 
                 suspectNamesFile, dateValidation, dateTimeSpanValidation, maxFileSize, 
                 escala, 
                 subject, rootOwnerMail, rootCCMail, rootBCCMail, replytoAddrs, 
                 isDebug):
   suspectWords = getList(suspectNamesFile)
   
   fileSizeAverage = 0
   fileSizeTotal = 0
   fileCount = 0
   filesizeProbabList = dict()
   filesReportName = dict()
   filesReportSize = dict()
   filesReportProbability = dict()
   
   for (root, dirnames, filenames) in os.walk(rootSetor):   
      for filename in filenames:
         fileuri = os.path.join(root, filename)
         # Para exibição no email
         fileShow = fileuri.replace(rootSetor, rootShow).replace("/", settings.separador)
         filesize = -1      
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
   
         # So analisa os arquivos que estao compreendidos no timespan definido
         if (dateFlag):
            if (filesize >= maxFileSize*escala):
               filesReportSize[fileShow] = filesize

#             Só entra na lista se possuir alguma palavra suspeita
            suspectCounter = 0
            for suspectword in suspectWords:
               if (suspectword.upper() in filename.upper()):
                  suspectCounter = suspectCounter + 1                  
                  filesizeProbabList[fileShow] = filesize                  
                  # Debugging
                  # print ('%d - %d\n' % (filename, suspectword))
            if suspectCounter > 0:
               filesReportName[fileShow] = suspectCounter               

            # Só vale a pena se existir um t
            if (suspectCounter > 1 or filesize > 0):
               probability = suspectFileProbability(suspectCounter, filesize/escala)
               if probability > 0.05:
                  filesizeProbabList[fileShow] = filesize
                  filesReportProbability[fileShow] = probability

   
   if (fileCount > 0):
      fileSizeAverage = float(fileSizeTotal)/float(fileCount)      

      # Escrevendo o corpo do email
      fileProblems = settings.mailBody(fileSizeAverage, escala, fileCount, fileSizeTotal)
      
      sendMailFlag = False
      
      #Sorting by Probability
      if len(filesReportProbability) > 0:
         filesReportProbabilityLista = sorted(filesReportProbability.items(), key=operator.itemgetter(1), reverse=True)
         fileProblems = (fileProblems + 
                         "%sArquivos com maior probabilidade de serem suspeitos: \n Tamanho | %% | #Termos | Caminho do arquivo %s" % 
                         (settings.lineBreaker, settings.lineBreaker))
         for key in filesReportProbabilityLista:
            probability = key[1]
            size = float(filesizeProbabList[key[0]])/(escala)
            aux = ('%5.2f MB| %2.2f %% | %d |' % (size, probability*100, filesReportName[key[0]]))
            fileProblems =  fileProblems + aux + key[0] + "\n"
         sendMailFlag = True
      
      #Sorting by size
      if len(filesReportSize) > 0:
         
         filesReportSizeLista = sorted(filesReportSize.items(), key=operator.itemgetter(1), reverse=True)
         fileProblems = (fileProblems + 
                         ("%sArquivos com tamanhos suspeitos (Acima de %d MB): \nTamanho | Caminho do arquivo%s" % 
                          (settings.lineBreaker, maxFileSize, settings.lineBreaker)))
         for key in filesReportSizeLista:    
            fileProblems =  fileProblems + '%5.2f MB | ' %  float(float(key[1])/(escala)) + key [0]+ "\n"
         sendMailFlag = True
      
      #Sorting by Name
      if len(filesReportName) > 0:
         
         filesReportNameLista = sorted(filesReportName.items(), key=operator.itemgetter(1), reverse=True)
         fileProblems = (fileProblems + 
                         "%sArquivos com nomes suspeitos: \nTamanho | #Termos | Caminho do arquivo%s" % 
                         (settings.lineBreaker, settings.lineBreaker))
         for key in filesReportNameLista:
            fileProblems =  fileProblems + ('%5.2f MB | %d |' %  (float(float(filesizeProbabList[key[0]])/(escala)), filesReportName[key[0]])) + key[0] + "\n"
         sendMailFlag = True
          

      if sendMailFlag:
         sendEmail (settings.systemMail, 
            rootOwnerMail, rootCCMail, rootBCCMail, settings.replyToMail, 
            subject, fileProblems, 
            settings.systemMail, settings.systemPasswd, settings.smtpServer, settings.smtpPort, isDebug)
   else:
      print "Pasta \"%s\" não encontrada! " % rootSetor
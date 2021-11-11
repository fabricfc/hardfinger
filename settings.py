#!-*- coding: utf8 -*
import sys
sys.path.append('./file/')
sys.path.append('./mail/')
sys.path.append('./searchengine/')

isDebug = False
#isDebug = True

# Megabytes
escalaKB = 1024 ** 1 # Kilobytes
escalaMB = 1024 ** 2 # Megabytes
escalaGB = 1024 ** 3 # Gibabytes

separador = "\\"

lineBreaker = "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"

# Send mail settings 
smtpServer = 'smtp.gmail.com'
smtpPort = 587
systemMail = 'user@gmail.com'
systemPasswd = 'email-password'
replyToMail = ["email2reply@gmail.com"]

def mailBody(fileSizeAverage, escala, fileCount, fileSizeTotal): 
   return ("Prezado Gestor,\n\n" + 
                      "\t Visando uma melhor utilização do espaço da pasta do setor (no servidor de arquivos), " + 
                      "trouxemos uma lista com o tamanho e o nome dos arquivos que podem causar " +
                      "falta de espaço e alguns problemas legais (que podem estar violando a política de utilização). \n\n" + 
                      "\t Assim, sugerimos que veja cautelosamente se os arquivos devem permanecer na pasta do setor e solicite, " + 
                      "caso necessário, a remoção do arquivo à pessoa que o colocou." +
                      "\n\n" +
                      "Atenciosamente, \n Equipe da TI" +
                      "\n\n") + ("Tamanho médio: %0.2f MB | (Total de arquivos: %d) | (Uso de disco: %0.2f MB) \n" % 
              (fileSizeAverage/(escala), fileCount, fileSizeTotal/(escala)))

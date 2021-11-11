#!-*- coding: utf8 -*
import smtplib

def messageFormat (fromaddr, toAddrs, ccAddrs, bccAdrss, replytoAddrs, subject, msg):
   return "\r\n".join([
     "From: " + fromaddr,
     "To: " + ", ".join(toAddrs),
     "CC: " + ", ".join(ccAddrs),
     #"Bcc: " + ", ".join(bccAdrss),
     "reply-to: " + ", ".join(replytoAddrs),     
     "Subject: " + subject,
     "\r\n",
     msg 
   ])

def sendEmail (fromAddr, 
               toAddrs, ccAddrs, bccAdrss, replytoAddrs,
               subject, msg, 
               mailUser, mailPasswd, smtpServer, smtpPort,
               isDebug):
   
   if (not isDebug):
      server = smtplib.SMTP(smtpServer, smtpPort)
      server.ehlo()
      server.starttls()
      server.login(mailUser, mailPasswd)
      server.sendmail(fromAddr, toAddrs + ccAddrs + bccAdrss, 
                      messageFormat(fromAddr, toAddrs, ccAddrs, bccAdrss, replytoAddrs, subject, msg))
      server.quit()
   else:
      print messageFormat(fromAddr, toAddrs, ccAddrs, bccAdrss, replytoAddrs, subject, msg)

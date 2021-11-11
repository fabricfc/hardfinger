#!-*- coding: utf8 -*
from scipy import stats


def suspectFileProbability(nmbrSuspectWords, fileSize):
#    Filesize parameter
   p_size = stats.chi2.cdf(fileSize*10/1024, 3)
   n_p_size = 1 - p_size 
   
#    Nmbr of suspect words
   p_suspect = stats.chi2.cdf(nmbrSuspectWords, 2)   
   n_p_suspect = 1 - p_suspect
   
   p_true = p_size * p_suspect
   p_false = n_p_size * n_p_suspect

   return p_true / (p_true + p_false)

# print suspectFileProbability(3, 300)
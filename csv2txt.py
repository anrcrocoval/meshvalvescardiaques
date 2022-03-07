# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:18:10 2022

@author: emile
"""


import csv


def conversion(nomSansExtension):
    fileCsv = open(nomSansExtension + '.csv')
    csvreader = csv.reader(fileCsv)
    header = next(csvreader)
    
    fileTxt = open(nomSansExtension + '.txt', 'w') 
    nbPts = 1
    
    for row in csvreader:
        if row != []: # dernière ligne est vide
            ligne = row[0]
            coos = []
            i = 0
            for j in range(3):
                mot = ''
                while ligne[i] != '\t':
                    mot += ligne[i]
                    i += 1
                coos.append(float(mot))
                i += 1
            #on a récup les coordonnées
            fileTxt.write('//+\n')
            fileTxt.write('Point(' + str(nbPts) + ') = {' + str(coos[0]) + ', ' + str(coos[1]) + ', ' + str(coos[2]) + ', 1.0};\n')
            nbPts += 1
                                       
    fileCsv.close()
    fileTxt.close()
    
    
nom = 'resultline'
for i in range(1,10):
    nomSansExtension = nom + str(i)
    conversion(nomSansExtension)



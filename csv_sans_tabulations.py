# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 22:33:54 2022

@author: emile

Transforme un fichier .csv de nuage de points avec tabulations en fichier .csv
classique avec des virgules
"""



import csv


def conversion(nomSansExtension):
    fileCsv = open(nomSansExtension + '.csv')
    csvreader = csv.reader(fileCsv)    
    fileTxt = open(nomSansExtension + 'SansTabulation.csv', 'w') 
    
    for row in csvreader:
        if row != []: # dernière ligne est vide
            ligne = row[0]
            nouvelleLigne = ''
            i = 0
            for j in range(3):
                mot = ''
                while ligne[i] != '\t':
                    mot += ligne[i]
                    i += 1
                
                nouvelleLigne += mot
                if j!= 2:
                    nouvelleLigne += ','
                i += 1
            #on a récup les coordonnées
            fileTxt.write(nouvelleLigne)
            fileTxt.write('\n')
                                      
    fileCsv.close()
    fileTxt.close()
    
    
nom = 'resultline1'
conversion(nom)

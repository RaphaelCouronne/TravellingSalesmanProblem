# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:20:17 2019

@author: Lara
"""

from common import *
import time

import math

#def Sommets_Graphe_Alea(n):
#    """ détermine les sommets aléatoires par la loi uniforme sur le carré [0,100]**2"""
 #   return [[uniform(0,100),uniform(0,100)] for k in range(n)]


#On stocke chaque point sous forme d'une liste de 2 coordonnées

def Distance_Chemin(A, B):
    return math.sqrt((B[0]-A[0])**2+(B[1]-A[1])**2)
    
def Distance_Trajectoire(sommets):
    # sommets est une liste de points (tuples)
    # calculer la somme des distance sur les chemins
    # ne pas oublier la distrance du dernier au premier!
    return 0
    
# def Chemins(sommets):
#     if n == 2:
#         return [[0]]
#     else: u = [sommets]
#     for point in sommets:
#         for k in range(len(sommets)):
            
            
        
    
#def Voyageur_de_commerce(sommets):
#    distance_min = Distance_trajectoires(sommets)
#    chemin_min = sommets
#    for k in range(len(sommets)-1):
#        if 

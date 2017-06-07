# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:07:05 2017

@author: henry
"""

class noeud_opt: 
    
    
    def __init__(self, nom, ligne_script):
        self.nom = nom
        self. ligne_script = ligne_script
        self.fils = []
        #self.parent = []
    
    """def add_parent(self, noeud):
        self.parent.append(noeud)"""
        

    def add_fils(self, noeud):
        self.fils.append(noeud)

    def print_arbre(self):
        result = [self.nom + '_' + str(self.ligne_script)]
        if len(self.fils) != 0:
            for i in self.fils:
                result.append(i.print_arbre())
            
        return result

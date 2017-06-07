# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:56:40 2017

@author: petrucusnir
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
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:07:05 2017

@author: henry
"""

class noeud_opt: 
    
    
    def _init_(self, nom, ligne_script):
        self.nom = nom
        self. ligne_script = ligne_script
        self.fils = []
        #self.parent = []
    
    """def add_parent(self, noeud):
        self.parent.append(noeud)"""
        
        def add_fils(self, noeud):
            sefl.fils.append(noeud)
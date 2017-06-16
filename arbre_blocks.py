# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:18:29 2017

@author: gabriel & petrucusnir
"""

class noeud_block: 
    
    
    def __init__(self, _id):
        self.arbreopti = None
        self.arrivalgate = None
        self.contenu = None
        self.destinationgate = None
        self.id = _id
        self.fils = []
    
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
        
    '''#deffinition du arrivalgate :
    def determine_arrivalgate(self):     
        liste = self.contenu.split("\n")
        result = []
        for i in range(len(liste)):
            if ":" in liste[i]:
                self.arrivalgates = liste[i]'''

            
        
    #recherche le noeud contenant l'addresse destination du jump
    '''def recherche_parArrivalGate(self, string):
        result = []
        for i in range(len(self.arrivalgates)):
            if string in self.arrivalgates[i]:
                result.append(self)
        else :
            for i in range(len(self.fils)):
                result.extend(self.fils[i].recherche_parArrivalGate(string))
        for x in result :
            print('#########################' + x.nomJ + '######################')
        return result'''
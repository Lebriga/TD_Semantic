# -*- coding: utf-8 -*-
"""
Created on Wed May 17 08:11:17 2017

@author: François


"""

import re
'''m = search(r'(\s)+:', line)
if m:
    m.groupe(1)'''
    

class AST:
    
    idWhile = 0
    
    def __init__(self, _type, _value):
        self.type = _type
        self.value = _value
        self.sons = []
        
    def __str__(self):
        
        return "%s%s" % (self.value, self.sons)
    
    def __repr__(self):
        
        return "%s%s" % (self.value, self.sons)

    def e_toASM(self):
        
        if self.type == "NUMBER":
            return "mov eax, %s\n" % self.value
            
        elif self.type == "ID":
            return "mov eax, [%s]\n" % self.value
            
        elif self.type == "OPBIN":
            op1 = self.sons[0].e_toASM()
            op2 = self.sons[1].e_toASM()
            
            if self.value == '+':
                res = "%spush eax\n%spop ebx\nadd eax, ebx\n" % (op1, op2)
            else:
                res = "%spush eax\n%spop ebx\nsub eax, ebx\n" % (op2, op1)
            return res
    
    def c_toASM(self):
        
        if self.value == "=":
            return "%s\nmov[%s], eax" % (self.sons[1].e_toASM(), self.sons[0])
        
        elif self.value == ';':
            return"%s\n%s" % (self.sons[0].c_toASM(), self.sons[1].c_toASM())
            
        else:
            AST.idWhile += 1
            return """debutboucle%s:
%s
cmp eax, 0
jz finboucle%s
%s
jmp debutboucle%s
finboucle%s:
""" % (AST.idWhile, self.sons[0].e_toASM(), AST.idWhile, self.sons[1].c_toASM(), AST.idWhile, AST.idWhile)


    def fvars(self):
        var = set()
        if self.type == "programme":
            var.update(self.sons[0])
            var.update(self.sons[1].fvars())
            var.update(self.sons[2].fvars())
            return var
        
        elif self.type == "AFFECT":
            var.add(self.sons[0])
            var.update(self.sons[1].fvars())
            return var
            
        elif self.value == "while":
            var.update(self.sons[0].fvars())
            var.update(self.sons[1].fvars())
            return var
    
        elif self.type == "END":
            var.update(self.sons[0].fvars())
            var.update(self.sons[1].fvars())
            return var
            
        elif self.type == "OPBIN":
            var.update(self.sons[0].fvars())
            var.update(self.sons[1].fvars())
            return var
            
        elif self.type == "NUMBER":
            return var
            
        else:
            var.add(self.value)
            return var
            
            
    def init_var(self, var, i):
        return """mov ebx, [eax + %s]
push eax
push ebx
call atoi
add esp, 4
mov [%s], eax
pop eax
""" % (str(4*(i+1)), var)
        
    def init_vars(self, motif):
        motif = motif.replace("LEN_INPUT", str(len(self.sons[0])))
        init = [self.init_var(self.sons[0][i], i) for i in range(len(self.sons[0]))]
        motif = motif.replace("VAR_INIT", "\n".join(init))
        return motif
            
    def p_toASM(self):
        ## Ouverture Lecture
        f = open("motif.asm")
        motif = f.read()
        
        ## Création liste variable
        var = self.fvars()
        dvar = {"%s: dd 0" % v for v in var}
        var_decl = "\n".join(dvar)
        motif = motif.replace("VAR_DECL", var_decl)
        motif = self.init_vars(motif)
        
        ## Commande
        motif = motif.replace("COMMAND_EXEC", self.sons[1].c_toASM())
        
        ## Evaluation
        motif = motif.replace("EVAL_OUTPUT", self.sons[2].e_toASM())
        
        #optimization
        motif = optimize(motif)        
        
        g = open("motifrempli.asm", "w")
        g.write(motif)

        return motif
   
 ####################################
 ###################################
 ###################################
import arbre_opti
import arbre_blocks

#fonction qui attribue un departureGate à chaque noeud, nécessaire car departure gate d'un block c'est le début du suivant en raison du split selon jmp...
def ajouteur_de_departureGate(listeBlocks):
    for i in range(len(listeBlocks)-1):
        destiny = listeBlocks[i+1].contenu.split("\n") #obtention contenu splitté selon lignes
        listeBlocks[i].destinationgate = destiny[0] #destinationgate du block i devient première ligne du block i+1
        
#fonction qui prend la liste des blocks, la parcours et détermine et attribue les fils de chaque noeud
def ajouteur_de_fils(listeBlocks):
    for i in listeBlocks:
        for j in listeBlocks:
            for y in j.arrivalgates:
                if i.destinationgate :
                    print('----------------------', i.destinationgate, '--------------------------', y)
                    if i.destinationgate[1:] in y :
                        print('#############################')                        
    return None

def optimize(motif):
    #Premiere ligne sert à splitter en fonciton de jump le string en liste de strings
    liste = re.split(":", motif)
    for i in liste:
        i.split("jmp")


    for i in liste:
        for j in i:
            print('-----------------------')
            print(j)
            print('-----------------------')
            
    #Ne pas enlever cette ligne à la fin de la fonction
    for j in liste:
        j = "jmp".join(j)
    liste = ":".join(liste)
    return liste  
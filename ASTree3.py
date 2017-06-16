# -*- coding: utf-8 -*-
"""
Created on Wed May 17 08:11:17 2017

@author: François


"""
'''
import re
m = search(r'(\s)+:', line)
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


        print('Je suis dans le bon ASTree')
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
import re


def optimize(motif):

    '''A supprimer!
    #Premiere ligne sert à splitter en fonciton de jump le string en liste de strings
    liste = motif.split("jmp")
    '''

    #liste des noeuds dans l'ordre pour reconstruction syntaxique
    listeblocks = []

    #RacineBlock = arbre_blocks.noeud_block(-1)

    (initialisation, Lparse) = create_arbre(motif, listeblocks)
    
    
    for i in range(len(listeblocks)):
        print("---------------------")
        #print("---------------------")
        #print(listeblocks[i].arrivalgate)
        #print(listeblocks[i].destinationgate)
        #print("---------------------")
        print(listeblocks[i].contenu)
    
    #traitent de chaque contenu de chaque block    
    traiter_arbre(listeblocks)
    
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('-------------------------------------------')
    
    for i in range(len(listeblocks)):
        print("---------------------")
        #print("---------------------")
        #print(listeblocks[i].arrivalgate)
        #print(listeblocks[i].destinationgate)
        #print("---------------------")
        print(listeblocks[i].contenu)
        
    #reassemblage final
    testlist = []
    for x in listeblocks:
        testlist.append(x.contenu)
    
    return "\n".join(testlist)
    
def traiter_arbre(liste_blocks):
    for i in liste_blocks:
        i.traitement()

def create_arbre(motif, liste_blocks):
    #Sépare la phase d'initialisation du corps du programme :
    A = motif.split('main:')
    if len(A)>1:
        initialisation = A[0] + 'main:'
    else :
        print('Error : Absence de "main:')
    #Parse motif en séparant les ":" et les "jmp"
    L = A[1].split('jmp')
    Lclefs = []
    result = []
    for i in range(len(L) - 1):
        Lclefs.append(L[i]+'jmp')
        Lclefs.append('jmp')
    Lclefs.append(L[-1])

    for i in Lclefs:
        l = i.split(':')
        for j in range(len(l) - 1):
            result.append(l[j] + ':')
            result.append(':')
        result.append(l[-1])
    j = 0

    #Crée les noeuds correspondant aux blocs
    for i in range (len(result)):
        if result[i] != 'jmp' and result[i] != ':':
            block = arbre_blocks.noeud_block(j)
            block.contenu = result[i]
            liste_blocks.append(block)
            j += 1
    
        #rajout des departureGate au noeuds
    ajouteur_de_arrivalGate(liste_blocks)
    
    #rajout des departureGate au noeuds
    ajouteur_de_departureGate(liste_blocks)
    
    ajouteur_de_fils(liste_blocks)    
    
    return(initialisation, result)
    

#fonction qui attribue un arribalGate à chaque noeud, nécessaire car arrival gate d'un block c'est la fin du précedent en raison du split selon jmp...
def ajouteur_de_arrivalGate(listeBlocks):
    for i in range(1,len(listeBlocks)-1):
        arrivee = listeBlocks[i-1].contenu.split("\n") #obtention contenu splitté selon lignes
        if ":" in arrivee[-1]:
            listeBlocks[i].arrivalgate = arrivee[-1] #destinationgate du block i devient première ligne du block i+1
        
#fonction qui attribue un departureGate à chaque noeud, nécessaire car departure gate d'un block c'est le début du suivant si il y a jmp a la fin du en-cours en raison du split selon jmp...
def ajouteur_de_departureGate(listeBlocks):
    for i in range(len(listeBlocks)-1):
        encours = listeBlocks[i].contenu.split("\n")
        if 'jmp' in encours[-1]:
            destiny = listeBlocks[i+1].contenu.split("\n") #obtention contenu splitté selon lignes            
            listeBlocks[i].destinationgate = destiny[0] #destinationgate du block i devient première ligne du block i+1
        
#fonction qui prend la liste des blocks, la parcours et détermine et attribue les fils de chaque noeud
def ajouteur_de_fils(listeBlocks):
    for i in listeBlocks:
        for j in listeBlocks:
            if i.destinationgate :
                if j.arrivalgate:
                    #print('----------------------', i.destinationgate[1:], '--------------------------', j.arrivalgate[0:-1])
                    if re.search('^'+ i.destinationgate[1:] +'$', j.arrivalgate[0:-1]) :
                        #print('#############################')
                        i.fils.append(j)
    return None

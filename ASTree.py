# -*- coding: utf-8 -*-
"""
Created on Wed May 17 08:11:17 2017

@author: François


"""
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

def optimize(motif):
    #Premiere ligne sert à splitter en fonciton de jump le string en liste de strings
    liste = motif.split("jmp")
    
    #application de la fonction traitment à chaque block
    for i in range(len(liste)):
        liste[i] = traitement(liste[i])
    
    #Ne pas enlever cette ligne à la fin de la fonction
    return "jmp".join(liste)


def traitement(string):
    #Premiere ligne sert à splitter en fonciton de \n le block en liste de strings
    liste = string.split("\n")
    #en plus de faire partie de l'arbre tous les noeuds representants une opération mov dans un registre seront rangés dans cette liste afin d'êtres parcourus à la fin pour s'assurer qu'ils ont en fils push, cmp, ou add, le cas contraire ils seront supprimés
    liste_noeuds = []
    #creation premier noeud de l'arbre du bloc
    racine = arbre_opti.noeud_opt('valeur', -1)
    #######################################
    #parcours du bloc et création de l'arbre
    for i in range(len(liste)):
        print("-------------------------")
        print(i)
        ligne = reconnait(liste[i])
        print(ligne)
        if ligne[0][0] == 'mov':
            # crée le nouveau noeud de nom : ligne[0][1]_i (nomregistre_numeroligne)
            noeud = arbre_opti.noeud_opt(ligne[0][1], i)
            # ajoute en tant que fils le noeud créé auparavant au dernier noeud de l'arbre représentant le registre ligne[1]
            recherchenoeud(liste_noeuds, ligne[1], racine).add_fils(noeud)
            # ajoute le noeud à la liste des noeuds
            liste_noeuds.append(noeud)
        #si push on rajoute un noeud push en fils de noeud pushé mais on NE rajoute PAS le noeud push à liste_noeud (liste des registres)
        elif ligne[0][0] == 'push':
            noeud = arbre_opti.noeud_opt('push', i)
            recherchenoeud(liste_noeuds, ligne[0][1], racine).add_fils(noeud)
        #idem mais pour cmp et il  a cette fois deux fils
        elif ligne[0][0] == 'cmp':
            noeud = arbre_opti.noeud_opt('cmp', i)
            recherchenoeud(liste_noeuds, ligne[0][1], racine).add_fils(noeud)
            recherchenoeud(liste_noeuds, ligne[1], racine).add_fils(noeud)
        #idem pour add mais il faut distinguer les add dans esp et les add dans un registre dans quel cas il faut qu'il soit push après
        elif ligne[0][0] == 'add':
            if ligne[0][1] == 'esp':
                noeud = arbre_opti.noeud_opt('add', i)
                recherchenoeud(liste_noeuds, ligne[1], racine).add_fils(noeud)
            else:
                noeud = arbre_opti.noeud_opt(ligne[0][1], i)
                recherchenoeud(liste_noeuds, ligne[1], racine).add_fils(noeud)
                liste_noeuds.append(noeud)
                
                

    print('---------------------------------------------------')
    print ('Arbre avant suppressions')
    print(racine.print_arbre())
    for n in liste_noeuds:
        print(n.nom + '_'+str(n.ligne_script))
    #######################
    #suppression des lignes
    #######################
    i = len(liste_noeuds) - 1
    while i>-1:
        l = liste_noeuds[i].fils
        print(liste_noeuds[i].nom + '_' + str(liste_noeuds[i].ligne_script))
        print(len(l))

        supprimes = True
        for j in range(len(l)):
            if l[j].nom != 'suppressed':
                supprimes = False
        if supprimes:
            print(liste_noeuds[i].nom +'_'+ str(liste_noeuds[i].ligne_script) + 'a été supprimé')
            liste_noeuds[i].suppress()
            liste[liste_noeuds[i].ligne_script] = ''
        i = i - 1




        print("-------------------------")
        print("Arbre après suppression")
        print(racine.print_arbre())
        print("---------------------------------------------------------------------------")
    
    print('------')
    print('Suppressions terminées')
    print('------')
    
    #Ne pas enlever cette ligne à la fin de la fonction
    return "\n".join(liste)

#separe phrase en [[1er terme, 2eme terme], valeur]
def reconnait(string):
    liste = string.split(",")
    liste[0] = liste[0].split(" ")
    #correction syntaxe : mov[x] := mov [x]
    if 'mov' in liste[0][0] and len(liste[0][0]) > 3:
        print('---------------------------------------------------Avant-----------------------------------------------------------------------------')
        print(liste)       
        liste[0].append(liste[0][0][3:])
        liste[0][0] = liste[0][0][0:3]


    #suppression espace valeur
    if len(liste) > 1:
        if liste[1][0] == " ":
            liste[1] = liste[1][1:]
    print('-----------------------------------------------------------------------------------------------------------------------------------------')
    print(liste)
    print('-----------------------------------------------------------------------------------------------------------------------------------------')
    return liste
    
def recherchenoeud(liste, nom, racine):
    i = len(liste) -1
    while i >= 0:
        if liste[i].nom == nom:
            return liste[i]
        i -=1
    return racine
    
###############################################################################
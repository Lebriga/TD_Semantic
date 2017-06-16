# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:18:29 2017

@author: gabriel & petrucusnir
"""
import arbre_opti

class noeud_block: 
    
    
    def __init__(self, _id):
        self.read = []
        self.wrote = []
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
        result = [self.id + '_' + self.contenu]
        if len(self.fils) != 0:
            for i in self.fils:
                result.append(i.print_arbre())     
        return result

#######################################"
    def traitement(self):
        #Premiere ligne sert à splitter en fonciton de \n le block en liste de strings
        liste = self.contenu.split("\n")
        #en plus de faire partie de l'arbre tous les noeuds representants une opération mov dans un registre seront rangés dans cette liste afin d'êtres parcourus à la fin pour s'assurer qu'ils ont en fils push, cmp, ou add, le cas contraire ils seront supprimés
        liste_noeuds = []
        #creation premier noeud de l'arbre du bloc
        racine = arbre_opti.noeud_opt('valeur', -1)
        #######################################
        #parcours du bloc et création de l'arbre
        for i in range(len(liste)):
            ligne = reconnait(liste[i])
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
        
        #####################
        #creation read/wrote pour trouver elements qui sont utilisés dans autres blocs
        #####################

        #remplisache liste des wrote
        y = len(liste_noeuds) - 1
        while y>-1:
            already_exists = False
            for m in self.wrote:
                if liste_noeuds[y].nom == m.nom:
                    already_exists = True      
            if not already_exists:
                self.wrote.append(liste_noeuds[y])
            y = y - 1
        '''print('----------')
        for n in self.wrote:
            print(n.nom)'''
        
        
        #remplissaage liste des read
        liste_overwrote = []
        for i in range(len(liste)):
            ligne = reconnait(liste[i])
            if len(ligne) > 1:
                already_exists_or_overwrote = False
                for m in self.read:
                    if ligne[1] == m:
                        already_exists_or_overwrote = True
                for m in liste_overwrote:
                    if ligne[1] == m:
                        already_exists_or_overwrote = True
                writing = racine.recherche_par_lignescript(i)
                if writing:
                    liste_overwrote.append(writing.nom)
                if not already_exists_or_overwrote:
                    self.read.append(ligne[1])
                print(i)
        print('__'.join(self.read))
                
                
            
            
    
        '''print('---------------------------------------------------')
        print ('Arbre avant suppressions')
        print(racine.print_arbre())
        for n in liste_noeuds:
            print(n.nom + '_'+str(n.ligne_script))'''
        #######################
        #suppression des lignes
        #######################
        i = len(liste_noeuds) - 1
        while i>-1:
            l = liste_noeuds[i].fils
            '''print(liste_noeuds[i].nom + '_' + str(liste_noeuds[i].ligne_script))
            print(len(l))'''
    
            supprimes = True
            for j in range(len(l)):
                if l[j].nom != 'suppressed':
                    supprimes = False
            if supprimes:
                #print(liste_noeuds[i].nom +'_'+ str(liste_noeuds[i].ligne_script) + 'a été supprimé')
                liste_noeuds[i].suppress()
                liste[liste_noeuds[i].ligne_script] = ''
            i = i - 1
    
    
    
    
            '''print("-------------------------")
            print("Arbre après suppression")
            print(racine.print_arbre())
            print("---------------------------------------------------------------------------")
        
        print('------')
        print('Suppressions terminées')
        print('------')'''
        
        #Ne pas enlever cette ligne à la fin de la fonction
        self.contenu = "\n".join(liste)

#separe phrase en [[1er terme, 2eme terme], valeur]
def reconnait(string):
    liste = string.split(",")
    liste[0] = liste[0].split(" ")
    #correction syntaxe : mov[x] := mov [x]
    if 'mov' in liste[0][0] and len(liste[0][0]) > 3:
        '''print('---------------------------------------------------Avant-----------------------------------------------------------------------------')
        print(liste)'''       
        liste[0].append(liste[0][0][3:])
        liste[0][0] = liste[0][0][0:3]


    #suppression espace valeur
    if len(liste) > 1:
        if liste[1][0] == " ":
            liste[1] = liste[1][1:]
    '''print('-----------------------------------------------------------------------------------------------------------------------------------------')
    print(liste)
    print('-----------------------------------------------------------------------------------------------------------------------------------------')'''
    return liste
    
def recherchenoeud(liste, nom, racine):
    i = len(liste) -1
    while i >= 0:
        if liste[i].nom == nom:
            return liste[i]
        i -=1
    return racine

        
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
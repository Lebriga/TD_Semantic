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
        
        g = open("motifrempli.asm", "w")
        g.write(motif)
        print("------------------------------------")
        print(optimize(motif))
        print("------------------------------------")
        return motif
   
     
def optimize(motif):
    """Premiere ligne sert à splitter en fonciton de jump le string en liste de strings"""
    liste = motif.split("jmp")
    
    
    
    """Ne pas enlever cette ligne à la fin de la fonction"""
    return "jmp".join(liste)
        
        
        
        
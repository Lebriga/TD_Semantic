# TD_Semantic : Optimiser Assembleur

Notre rendu est compris dans 3 fichier : ASTree.py, arbre_blocks.py (contenant la classe de l'arbre des blocs) et arbre_opti.py (contenant la classe de l'arbre d'optimisation des lignes de chaque bloc). Il vous suffit d'éxecuter compilateur.py à partir du répertoire de notre rendu pour le tester. Nous avons travaillé avec la syntaxe de code du cours : 
<code>arbre = yacc.parse("main(X) {while(X) {Y=Y+1; X=X-1}; t = 3;; print(Y)}")</code>


<h2>Déroulement du Programme</h2>

Au sein de l'ASTree nous appelons notre fonction **optimize** sur le "motif" juste avant que **p_toASM** l'écrive dans le fichier asm.

La fonction **optimize** appele la fonction **create_arbre**(chargé de partager le code en blocs selon les jmp et les sections et de construire un arbre des blocs). C'est la fonction **create_arbre** qui appel les fonctions **ajouteur_de_arrivalGate**, **ajouteur_de_departureGate**, et **ajouteur_de_fils** chargés d'associer à chaque bloc les fils en fonction des blocs vers lesquels ils peuvent "jumper" (renvoyer) et des sections qu'ils representent.

Une fois l'arbre des blocs crée et les liaisons faites entre les nœuds **optimize** appel **traiter_arbre**. Cette dernière appel les méthodes **traitement**, **proteger** et **suppresion** pour chaque nœud de l'arbre des blocs chargés respectivement de construire l'arbre d'optimisation pour chaque bloc, de protéger de la suppression les lignes ayant une utilité dans un bloc fils, et enfin de supprimer effectivement les lignes rébarbatives.

Pour finir **optimize** réassemble le contenu de chaque bloc en un seul string et le return. 

<h2>Resultat</h2>

Pour comparer notre rendu vous pouvez comparer "motifsrempli.asm" avec "motifsrempli_ancienneVesion.asm".

Nous passons ainsi de 15 "mov" à 9.

<h4>Nouvelle Version :</h4>
<pre><code>
global main 
extern printf, atoi

section .data
message: db 'Hello World %d', 10, 0
message_erreur: db "Il y a %d arguments requis", 10, 0
X: dd 0
Y: dd 0
t: dd 0

section .text
main:

mov eax, [esp + 4]
cmp eax, 1 + 1
mov eax, [esp + 8]
jne erreur_nb_entree
mov ebx, [eax + 4]
push eax
push ebx
call atoi
add esp, 4

pop eax

jmp debut_prog
erreur_nb_entree:
mov eax, 1
push eax
lea eax, [message_erreur]
push eax
call printf
add esp, 8
jmp fin

debut_prog:
debutboucle1:
mov eax, [X]

cmp eax, 0
jz finboucle1
mov eax, [Y]
push eax

pop ebx
add eax, ebx


mov eax, 1
push eax
mov eax, [X]
pop ebx
sub eax, ebx


jmp debutboucle1
finboucle1:





mov eax, [Y]


push eax
lea eax, [message]
push eax
call printf
add esp, 8

fin: ret

</code></pre>


<h4>Ancienne Version :</h4>
<pre><code>
mov eax, [esp + 4]
cmp eax, 1 + 1
mov eax, [esp + 8]
jne erreur_nb_entree
mov ebx, [eax + 4]
push eax
push ebx
call atoi
add esp, 4

pop eax

jmp debut_prog
erreur_nb_entree:
mov eax, 1
push eax
lea eax, [message_erreur]
push eax
call printf
add esp, 8
jmp fin

debut_prog:
debutboucle1:
mov eax, [X]

cmp eax, 0
jz finboucle1
mov eax, [Y]
push eax

pop ebx
add eax, ebx


mov eax, 1
push eax
mov eax, [X]
pop ebx
sub eax, ebx


jmp debutboucle1
finboucle1:





mov eax, [Y]


push eax
lea eax, [message]
push eax
call printf
add esp, 8

fin: ret
</code></pre>

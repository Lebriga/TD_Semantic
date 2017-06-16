

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

jmp
 debut_prog
erreur_nb_entree:

mov eax, 1
push eax
lea eax, [message_erreur]
push eax
call printf
add esp, 8
jmp
 fin

debut_prog:

debutboucle1:

mov eax, [X]

cmp eax, 0
jz finboucle1
mov eax, [Y]
push eax

pop ebx



mov eax, 1
push eax

pop ebx
sub eax, ebx


jmp
 debutboucle1
finboucle1:






mov eax, [Y]


push eax
lea eax, [message]
push eax
call printf
add esp, 8

fin:
 ret


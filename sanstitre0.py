# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:33:33 2017

@author: henry
"""

chaine = 'jumpafrz jump azdchibdskjnzaf : azpojfevrnfsdozdi hbaopzdofuhzjumpazbhdhbqs  auhf : aifjz azfea: earaz :ra arz rujnazdfjimpadbcfbzjump\najzdbc ajump'

result = []
L = chaine.split('jump')
Lclefs = []
for i in range(len(L)-1) :
    Lclefs.append(L[i])
    Lclefs.append('jump')
Lclefs.append(L[-1])

for i in Lclefs:
    l = i.split(':')
    for j in range(len(l)-1) :
        result.append(l[j])
        result.append(':')
    result.append(l[-1])

print(result)
    
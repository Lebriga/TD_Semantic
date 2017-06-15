
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programmeNUMBER ID OPBIN LPAREN RPAREN LACO RACO END AFFECT COMMA FINISH WHILE MAIN PRINT RETURN IFprogramme : MAIN LPAREN enum RPAREN LACO commande FINISH PRINT LPAREN expression RPAREN RACO\n    enum : ID\n              | ID COMMA enum\n    empty :commande : ID AFFECT expression\n                  | commande END commande\n                  | WHILE LPAREN expression RPAREN LACO commande RACOexpression :  NUMBER\n                    | ID\n                    | expression OPBIN expression'
    
_lr_action_items = {'LPAREN':([2,12,18,],[3,16,23,]),'END':([10,17,19,20,21,27,30,32,],[13,13,-8,-5,-9,-10,13,-7,]),'LACO':([7,25,],[9,28,]),'ID':([3,6,9,13,15,16,23,24,28,],[4,4,11,11,21,21,21,21,11,]),'RPAREN':([4,5,8,19,21,22,26,27,],[-2,7,-3,-8,-9,25,29,-10,]),'COMMA':([4,],[6,]),'RACO':([17,19,20,21,27,29,30,32,],[-6,-8,-5,-9,-10,31,32,-7,]),'PRINT':([14,],[18,]),'AFFECT':([11,],[15,]),'NUMBER':([15,16,23,24,],[19,19,19,19,]),'OPBIN':([19,20,21,22,26,27,],[-8,24,-9,24,24,24,]),'WHILE':([9,13,28,],[12,12,12,]),'MAIN':([0,],[2,]),'FINISH':([10,17,19,20,21,27,32,],[14,-6,-8,-5,-9,-10,-7,]),'$end':([1,31,],[0,-1,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'commande':([9,13,28,],[10,17,30,]),'programme':([0,],[1,]),'enum':([3,6,],[5,8,]),'expression':([15,16,23,24,],[20,22,26,27,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programme","S'",1,None,None,None),
  ('programme -> MAIN LPAREN enum RPAREN LACO commande FINISH PRINT LPAREN expression RPAREN RACO','programme',12,'p_programme','compilateur.py',83),
  ('enum -> ID','enum',1,'p_enum','compilateur.py',92),
  ('enum -> ID COMMA enum','enum',3,'p_enum','compilateur.py',93),
  ('empty -> <empty>','empty',0,'p_empty','compilateur.py',102),
  ('commande -> ID AFFECT expression','commande',3,'p_commande','compilateur.py',105),
  ('commande -> commande END commande','commande',3,'p_commande','compilateur.py',106),
  ('commande -> WHILE LPAREN expression RPAREN LACO commande RACO','commande',7,'p_commande','compilateur.py',107),
  ('expression -> NUMBER','expression',1,'p_expression','compilateur.py',123),
  ('expression -> ID','expression',1,'p_expression','compilateur.py',124),
  ('expression -> expression OPBIN expression','expression',3,'p_expression','compilateur.py',125),
]

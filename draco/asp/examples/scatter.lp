attribute(number_rows,root,100).

entity(field,root,f0).
attribute((field,name),f0,temp_max).
attribute((field,type),f0,number).

entity(field,root,f1).
attribute((field,name),f1,precipitation).
attribute((field,type),f1,number).

entity(view,root,v0).

entity(mark,v0,m).
entity(encoding,m,e0).
attribute((encoding,field),e0,temp_max).
entity(encoding,m,e1).
attribute((encoding,field),e1,precipitation).

#show entity/3.
#show attribute/3.

attribute(number_rows,root,100).

entity(field,root,f0).
attribute((field,name),f0,temperature).
attribute((field,type),f0,number).

entity(mark,root,m).
entity(encoding,m,e0).
attribute((encoding,field),e0,f0).

#show entity/3.
#show attribute/3.

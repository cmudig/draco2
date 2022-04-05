attribute(number_rows,root,100).

entity(field,root,(f,0)).
attribute((field,name),(f,0),temperature).
attribute((field,type),(f,0),number).

entity(mark,root,(m,0)).
entity(encoding,(m,0),(e,0)).
attribute((encoding,field),(e,0),(f,0)).

#show entity/3.
#show attribute/3.

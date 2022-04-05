attribute(number_rows,root,100).

entity(field,root,(f,0)).
attribute((field,name),(f,0),temperature).
attribute((field,type),(f,0),number).

entity(field,root,(f,1)).
attribute((field,name),(f,1),precipitation).
attribute((field,type),(f,1),number).

entity(view,root,(v,0)).
entity(mark,(v,0),(m,0)).
entity(encoding,(m,0),(e,0)).
attribute((encoding,field),(e,0),(f,0)).
entity(encoding,(m,0),(e,1)).
attribute((encoding,field),(e,1),(f,1)).

entity(scale,(v,0),(s,0)).
entity(scale,(v,0),(s,1)).

#show entity/3.
#show attribute/3.

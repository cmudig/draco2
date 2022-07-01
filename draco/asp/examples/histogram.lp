attribute(number_rows,root,100).

entity(field,root,(f,0)).
attribute((field,name),(f,0),temperature).
attribute((field,type),(f,0),number).
attribute((field,unique),(f,0),100).

entity(view,root,(v,0)).

entity(mark,(v,0),(m,0)).
entity(encoding,(m,0),(e,0)).
attribute((encoding,field),(e,0),(f,0)).
attribute((encoding,binning),(e,0),10).

#show entity/3.
#show attribute/3.

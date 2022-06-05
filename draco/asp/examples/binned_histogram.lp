attribute(number_rows,root,100).

entity(field,root,(f,0)).
attribute((field,name),(f,0),temperature).
attribute((field,type),(f,0),number).

entity(view,root,(v,0)).

entity(mark,(v,0),(m,0)).
attribute((mark,type),(m,0),bar).

entity(encoding,(m,0),(e,0)).
attribute((encoding,channel),(e,0),x).
attribute((encoding,field),(e,0),(f,0)).
attribute((encoding,binning),(e,0),10).

entity(encoding,(m,0),(e,1)).
attribute((encoding,channel),(e,1),y).
attribute((encoding,aggregate),(e,1),count).

entity(scale,root,(s,0)).
attribute((scale,channel),(s,0),x).
attribute((scale,type),(s,0),linear).

entity(scale,root,(s,1)).
attribute((scale,channel),(s,1),y).
attribute((scale,type),(s,1),linear).

#show entity/3.
#show attribute/3.

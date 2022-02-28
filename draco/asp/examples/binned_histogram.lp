attribute(number_rows,root,100).

entity(field,root,0).
attribute((field,name),0,temperature).
attribute((field,type),0,number).

entity(mark,root,1).
attribute((mark,type),1,bar).

entity(encoding,1,2).
attribute((encoding,channel),2,x).
attribute((encoding,field),2,temperature).
attribute((encoding,binning),2,10).

entity(encoding,1,3).
attribute((encoding,channel),3,y).
attribute((encoding,aggregate),3,count).

entity(scale,root,4).
attribute((scale,channel),4,x).
attribute((scale,type),4,linear).

entity(scale,root,5).
attribute((scale,channel),5,y).
attribute((scale,type),5,linear).

#show entity/3.
#show attribute/3.

% ====== Generators ======

% @generator(task) The task the viewer is trying to complete.
{ attribute(task,root,T) : domain(task,T) } = 1.

% @generator(mark_type) Marktype.
{ attribute((mark,type),M,T) : domain((mark,type),T) } = 1 :- entity(mark,_,M).

% @generator(encodings) Encodings of data fields as visual values.

% maximum number for each multi channel encoding
#const max_extra_encs = 5.

obj_id(1..max_extra_encs).

{ encoding(E): obj_id(E) }.

{ entity(encoding,M,E) : obj_id(E), entity(mark,_,M) }.

% use smaller ids first
:- not entity(encoding,_,ID), entity(encoding,_,ID-1), obj_id(ID), obj_id(ID-1).

% do not use the same encoding for different views
:- entity(encoding,V1,E), entity(encoding,V2,E), V1 != V2.

% @generator(channel) Visual encoding channel.
{ attribute((encoding,channel),E,C): domain((encoding,channel),C) } = 1 :- entity(encoding,_,E).

% @generator(field) The field to encode data from.
0 { attribute((encoding,field),E,F): domain((encoding,field),F) } 1 :- entity(encoding,_,E).

% @generator(field) Aggregation of the field.
0 { attribute((encoding,aggregate),E,A): domain((encoding,aggregate),A) } 1 :- entity(encoding,_,E).

% @generator(field) Binning of the data.
0 { attribute((encoding,binning),E,B): domain((encoding,binning),B) } 1 :- entity(encoding,_,E).

% ====== Generators ======

% @generator(mark_type) Marktype.
{ attribute(mark_type,V,M) : domain(mark_type, M) } = 1 :- property(view,root,V).

% @generator(encodings) Encodings of data fields as visual values.

% maximum number for each multi channel encoding
#const max_extra_encs = 5.

obj_id(1..max_extra_encs).

{ encoding(E): obj_id(E) }.

{ property(encoding,V,E) : obj_id(E), property(view,root,V) }.

% use smaller ids first
:- not property(encoding,_,ID)), property(encoding,_,ID-1), obj_id(ID), obj_id(ID-1).

% do not use the same encoding for different views
:- property(encoding,V1,E), property(encoding,V2,E), V1 != V2.

% @generator(channel) Visual encoding channel.
{ property(channel,E,C): domain(channel,C) } = 1 :- property(encoding,_,E).

% @generator(field) The field to encode data from.
0 { property(field,E,F): domain(field,F) } 1 :- property(encoding,_,E).

% @generator(field) Aggregation of the field.
0 { property(aggregate,E,A): domain(aggregate,A) } 1 :- property(encoding,_,E).

% @generator(field) Binning of the data.
0 { property(binning,E,A): domain(binning,A) } 1 :- property(encoding,_,E).


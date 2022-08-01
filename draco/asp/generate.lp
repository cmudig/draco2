% ====== Generators ======

% helpers to generate attributes based on whether they are required.
{ attribute(N,root,V) : domain(N,V) } = 1 :- root_required(N).
{ attribute((N,A),E,V): domain((N,A),V) } = 1 :- entity(N,_,E), required((N,A)).
0 { attribute((N,A),E,V): domain((N,A),V) } 1 :- entity(N,_,E), not_required((N,A)).

% maximum number of non-layered views.
#const max_views = 1.
{ entity(view,root,(v,0..max_views-1)) }.
:- { entity(view,root,_) } > max_views.
:- entity(view,root,(v,ID)), not entity(view,root,(v,ID-1)), ID > 0.

% maximum number of additional marks for each view.
#const max_marks = 2.
{ mark_id(V,0..max_marks-1) } :- entity(view,root,V).
:- mark_id(V,ID), not mark_id(V,ID-1), ID > 0.
{ entity(mark,V,(V,M)) } :- mark_id(V,M).

% maximum number for additional encoding channels.
#const max_encs = 4.
{ enc_id(M,0..max_encs-1) } :- entity(mark,V,M).
:- enc_id(M,ID), not mark_id(M,ID-1), ID > 0.
{ entity(encoding,M,(M,E)) } :- enc_id(M,E).

% @generate(encoding_channel) Each encoding requires a channel.
required((encoding,channel)).
% @generator(mark_type) Each mark requires a type.
required((mark,type)).
% @generator(task) Each root requires a task.
root_required(task).

% @generator(encoding_attribute) Encoding with binning, aggregate, field or stack.
not_required((encoding,binning)).
not_required((encoding,aggregate)).
not_required((encoding,field)).
not_required((encoding,stack)).

% generator(scale) generate scales such that their ids and channels corresponde to the encodings in each view.
{ entity(scale,V,(s,E)) } :- entity(mark,V,M), entity(encoding,M,E), attribute((encoding,channel),E,C).
attribute((scale,channel),(s,E),C) :- entity(scale,V,(s,E)), attribute((encoding,channel),E,C).

required((scale,channel)).
required((scale,type)).
not_required((scale,zero)).

% generator(facet) Each specification can have at most both row and col facet.
facet_id(0..1).
{ entity(facet,V,(fc,F)) : facet_id(F), entity(view,root,V) }.
:- entity(facet,V,(fc,1)), not entity(facet,V,(fc,0)),facet_id(1), facet_id(0).

required((facet,channel)).
required((facet,field)).
not_required((facet,binning)).

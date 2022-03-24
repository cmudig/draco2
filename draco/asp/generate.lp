% ====== Generators ======

% single view v0 on the root
{ entity(view,root,(v,0)) } = 1.

% maximum number of additional marks for each view
#const max_extra_marks = 1.
mark_id(0..max_extra_marks).
{ entity(mark,V,(m,M)) : entity(view,_,V), mark_id(M) }.
:- not entity(mark,_,(m,ID)), entity(mark,_,(m,ID-1)),mark_id(ID), mark_id(ID-1).

% maximum number for total encoding channels
#const max_extra_encs = 2.
encoding_id(M,E) :- entity(mark,_,(m,M)), N = 0..max_extra_encs, E = ((max_extra_encs + 1) * M) + N.
{ entity(encoding,(m,M),(e,E)) : entity(mark,_,(m,M)), encoding_id(M,E) }.
:- not entity(encoding,_,(e,ID)), entity(encoding,_,(e,ID-1)),encoding_id(_,ID), encoding_id(_,ID-1).

% @generate(encoding_channel) Each encoding requires a channel.
required((encoding,channel)).

% @generator(mark_type) Each mark requires a type.
required((mark,type)).
% @generator(task) Each root requires a task.
root_required(task).

% @generator(encoding_attribute) Encoding with binning, aggregate or field.
not_required((encoding,binning)).
not_required((encoding,aggregate)).
not_required((encoding,field)).

{ attribute(N,root,V) : domain(N,V) } = 1 :- root_required(N).
{ attribute((N,A),E,V): domain((N,A),V) } = 1 :- entity(N,_,E), required((N,A)).
0 { attribute((N,A),E,V): domain((N,A),V) } 1 :- entity(N,_,E), not_required((N,A)).

% generator(scale) Each view can only have less than 7 scales based on the domain of scale channels
{ entity(scale,V,(s,S)) : entity(view,_,V), S = 0..6 }.
{ attribute((scale,channel),S,C): domain((encoding_channel),V,C) } = 1 :- entity(scale,V,S).
{ attribute((scale,type),S,T): domain((scale,type),T) } = 1 :- entity(scale,V,S).

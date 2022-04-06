% ====== Generators ======

% helpers to generate attributes based on how they are required.
{ attribute(N,root,V) : domain(N,V) } = 1 :- root_required(N).
{ attribute((N,A),E,V): domain((N,A),V) } = 1 :- entity(N,_,E), required((N,A)).
0 { attribute((N,A),E,V): domain((N,A),V) } 1 :- entity(N,_,E), not_required((N,A)).

% single view v0 on the root
{ entity(view,root,(v,0)) } = 1.

% maximum number of additional marks for each view
#const max_extra_marks = 1.
mark_id(0..max_extra_marks).
{ entity(mark,V,(m,M)) : mark_id(M) } :- entity(view,_,V).
:- entity(mark,_,(m,ID)), not entity(mark,_,(m,ID-1)), mark_id(ID), mark_id(ID-1).

% maximum number for total encoding channels
#const max_extra_encs = 4.
encoding_id(M,E) :- entity(mark,_,(m,M)), N = 0..max_extra_encs, E = ((max_extra_encs + 1) * M) + N.
{ entity(encoding,(m,M),(e,E)) : encoding_id(M,E) }.
:- entity(encoding,(m,M),(e,ID)), not entity(encoding,(m,M),(e,ID-1)),encoding_id(M,ID), encoding_id(M,ID-1).

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
{ entity(scale,V,(s,E)) } = 1 :- entity(mark,V,M), entity(encoding,M,(e,E)), attribute((encoding,channel),(e,E),C).
attribute((scale,channel),(s,S),C) :- attribute((encoding,channel),(e,S),C).

required((scale,type)).

% generator(facet) Each specification can have at most both row and col facet.
facet_id(0..1).
{ entity(facet,V,(fc,F)) : facet_id(F), entity(view,root,V) }.
:- entity(facet,V,(fc,1)), not entity(facet,V,(fc,0)),facet_id(1), facet_id(0).

required((facet,channel)).
required((facet,field)).
not_required((facet,binning)).
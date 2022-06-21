% ====== Generators ======

% helpers to generate attributes based on whether they are required.
{ attribute(N,root,V) : domain(N,V) } = 1 :- root_required(N).
{ attribute((N,A),E,V): domain((N,A),V) } = 1 :- entity(N,_,E), required((N,A)).
0 { attribute((N,A),E,V): domain((N,A),V) } 1 :- entity(N,_,E), not_required((N,A)).

% single view v0 on the root
{ entity(view,root,(v,0)) } = 1.

% maximum number of non-layered views.
#const max_views = 1.
{ entity(view,root,(v,0..max_views-1)) }.
:- entity(view,root,(v,ID)), not entity(view,root,(v,ID-1)), ID > 1.

% maximum number of marks for each view
#const max_marks = 2.
{ entity(mark,(v,V),(m,V,0..max_marks-1)) : entity(view,_,(v,V)) }.
:- entity(mark,(v,V),(m,V,ID)), not entity(mark,(v,V),(m,V,ID-1)), ID > 1.

% maximum number for total encoding channels
#const max_encs = 4.
{ entity(encoding,(m,V,M),(e,V,M,0..max_encs-1)) : entity(mark,(v,V),(m,V,M)) }.
:- entity(encoding,(m,V,M),(e,V,M,ID)), not entity(encoding,(m,V,M),(e,V,M,ID-1)), ID > 1.


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
{ entity(scale,V,E) } = 1 :- entity(mark,V,M), entity(encoding,M,E), attribute((encoding,channel),E,C).
attribute((scale,channel),S,C) :- entity(scale,V,S), attribute((encoding,channel),S,C).

required((scale,type)).
not_required((scale,zero)).

% generator(facet) Each specification can have at most both row and col facet.
facet_id(0..1).
{ entity(facet,V,(fc,F)) : facet_id(F), entity(view,root,V) }.
:- entity(facet,V,(fc,1)), not entity(facet,V,(fc,0)),facet_id(1), facet_id(0).

required((facet,channel)).
required((facet,field)).
not_required((facet,binning)).
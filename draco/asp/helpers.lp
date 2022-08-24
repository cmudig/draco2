% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute((mark,channel),M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_with_stack) Whether a mark has an encoding with stacking.
attribute(mark_with_stack,M) :-
    entity(encoding,M,E),
    attribute((encoding,stack),E,_).

% @helper(mark_scale) Whether a mark has a scale.
attribute((mark,scale),M,S) :-
    entity(mark,V,M),
    entity(scale,V,S).
attribute((mark,scale),M,S) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,S).

% @helper(mark_scale_channel) Whether a mark has a scale type for a channel.
attribute(mark_scale_channel,M,T,C) :-
    attribute((mark,scale),M,S),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,T).

% @helper(mark_encoding_scale) Link mark, encoding, and scale togther.
attribute(mark_encoding_scale,M,E,S) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((mark,scale),M,S),
    attribute((scale,channel),S,C).

% @helper(encoding_type) Whether an encoding has a channel for a scale type.
attribute((encoding,scale_type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C).

% @helper(mark_channel_field) Whether a mark has an encoding for a field and a channel.
attribute(mark_channel_field,M,C,F) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,F).

% @helper(mark_channel_scale) whether a mark has a scale type for a channel(with or without binned encoding).
attribute(mark_channel_scale,M,T,C,B) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C),
    attribute((encoding,binning),E,B).
attribute(mark_channel_scale,M,T,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C),
    not attribute((encoding,binning),E,_).

% @helper(mark_channel_discrete_or_binned) Whether a mark has a discrete scale or binned encoding for a channel.
attribute(mark_channel_discrete_or_binned,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C),
    domain(discrete_scale,T).
attribute(mark_channel_discrete_or_binned,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,binning),E,_).

% @helper(mark_encoding_discrete_or_binned) Whether a mark has a discrete scale or binned encoding for an encoding.
attribute(mark_encoding_discrete_or_binned,M,E) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C),
    domain(discrete_scale,T).
attribute(mark_encoding_discrete_or_binned,M,E) :-
    entity(encoding,M,E),
    attribute((encoding,binning),E,_).

% @helper(mark_encoding_cont) Whether a mark has a continuous for an encoding.
attribute(mark_encoding_cont,M,E) :-
    entity(encoding,M,E),
    not attribute(mark_encoding_discrete_or_binned,M,E).

% @helper(mark_channel_cont) Whether a mark has a continuous scale for a channel.
attribute(mark_channel_cont,M,C) :-
    attribute((mark,channel),M,C),
    not attribute(mark_channel_discrete_or_binned,M,C).

% @helper(encoding_cardinality) The cardinality of an encoding.
attribute(encoding_cardinality,E,N) :-
    attribute((field,unique),F,N),
    attribute((encoding,field),E,F),
    not attribute((encoding,binning),E,_).
attribute(encoding_cardinality,E,N) :-
    attribute((encoding,binning),E,N).

% @helper(discrete_cardinality) The cardinality of a discrete encoding.
attribute(discrete_cardinality,M,E,N) :-
    attribute(encoding_cardinality,E,N),
    attribute(mark_encoding_discrete_or_binned,M,E).

% @helper(facet_cardinality,Fa,N) The cardinality of a facet.
attribute(facet_cardinality,Fa,N) :-
    attribute((field,unique),Fi,N),
    attribute((facet,field),Fa,Fi),
    not attribute((facet,binning),Fa,_).
attribute(facet_cardinality,Fa,N) :-
    attribute((facet,binning),Fa,N).

% @helper(is_c_c) Continuous by continuous.
attribute(is_c_c,M) :-
    entity(mark,_,M),
    attribute((mark,channel),M,x),
    attribute((mark,channel),M,y),
    not attribute(mark_channel_discrete_or_binned,M,x),
    not attribute(mark_channel_discrete_or_binned,M,y).

% @helper(is_c_d) Continuous by discrete (or only one continuous).
attribute(is_c_d,M) :-
    entity(mark,_,M),
    attribute(mark_channel_cont,M,x),
    not attribute(mark_channel_cont,M,y).
attribute(is_c_d,M) :-
    entity(mark,_,M),
    not attribute(mark_channel_cont,M,x),
    attribute(mark_channel_cont,M,y).

% @helper(is_d_d) Discrete by discrete.
attribute(is_d_d,M) :-
    attribute((mark,channel),M,x),
    attribute((mark,channel),M,y),
    attribute(mark_channel_discrete_or_binned,M,x),
    attribute(mark_channel_discrete_or_binned,M,y).
attribute(is_d_d,M) :-
    attribute((mark,channel),M,x),
    attribute(mark_channel_discrete_or_binned,M,x),
    not attribute((mark,channel),M,y).
attribute(is_d_d,M) :-
    attribute((mark,channel),M,y),
    attribute(mark_channel_discrete_or_binned,M,y),
    not attribute((mark,channel),M,x).

% @helper(non_pos_unaggregated) Non-positional channels are unaggregated.
attribute(non_pos_unaggregated,M) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    domain(non_positional,C),
    not attribute((encoding,aggregate),E,_).

% @helper(no_overlap) The continuous variable is a measure (it is aggregated) and all other non-positional channels are aggregated, or we use stack.
attribute(no_overlap,M) :-
    attribute(is_c_d,M),
    attribute(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,(x;y)),
    attribute((encoding,aggregate),E,_),
    not attribute(non_pos_unaggregated,M).
attribute(no_overlap,M) :-
    attribute(is_c_d,M),
    entity(encoding,M,E),
    attribute((encoding,stack),E,_).
attribute(no_overlap,M) :-
    attribute(is_c_d,M),
    attribute(number_rows,root,N),
    attribute(discrete_size,M,N).
attribute(no_overlap,M) :-
    attribute(is_d_d,M),
    attribute((mark,channel),M,C),
    domain(non_positional,C),
    not attribute(non_pos_unaggregated,M).
attribute(no_overlap,M) :-
    attribute(is_d_d,M),
    attribute(number_rows,root,N1),
    attribute(discrete_size,M,N2),
    N1 <= N2.

% @helper(overlap) We definitely overlap if the data size > discrete size.
attribute(overlap,M) :-
    attribute(is_c_d,M),
    not attribute(no_overlap,M),
    attribute(number_rows,root,N1),
    attribute(discrete_size,M,N2),
    N1 > N2.
attribute(overlap,M) :-
    entity(mark,V,M),
    attribute(is_d_d,M),
    not attribute(no_overlap,M),
    not entity(facet,V,_),
    attribute(number_rows,root,N1),
    attribute(discrete_size,M,N2),
    N1 > N2.

% @helper(discrete_size) The size of the discrete positional encoding.
attribute(discrete_size,M,N) :-
    attribute(is_c_d,M),
    attribute(x_cardinality,M,N).
attribute(discrete_size,M,N) :-
    attribute(is_c_d,M),
    attribute(y_cardinality,M,N).
attribute(discrete_size,M,1) :-
    attribute(is_c_d,M),
    attribute(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,x),
    not attribute((mark,channel),M,y).
attribute(discrete_size,M,1) :-
    attribute(is_c_d,M),
    attribute(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,y),
    not attribute((mark,channel),M,x).
attribute(discrete_size,M,N) :-
    attribute(is_d_d,M),
    attribute(x_cardinality,M,NX),
    attribute(y_cardinality,M,NY),
    N = NX*NY.

% @helper(x_cardinality) Cardinality of discrete x. Helps to go from quadratic to linear number of grounding.
attribute(x_cardinality,M,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,x),
    attribute(discrete_cardinality,M,E,N).
attribute(x_cardinality,M,1) :-
    entity(mark,_,M),
    not attribute((mark,channel),M,x).

% @helper(y_cardinality) Cardinality of discrete x. Helps to go from quadratic to linear number of grounding.
attribute(y_cardinality,M,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,y),
    attribute(discrete_cardinality,M,E,N).
attribute(y_cardinality,M,1) :-
    entity(mark,_,M),
    not attribute((mark,channel),M,y).

% @helper(enc_interesting)
attribute(enc_interesting,E) :-
    attribute((encoding,field),E,F),
    attribute((field,interesting),F,true).
attribute(enc_interesting,E) :-
    attribute((facet,field),E,F),
    attribute((field,interesting),F,true).
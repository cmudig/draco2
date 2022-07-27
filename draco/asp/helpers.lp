% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
helper((mark,channel),M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_with_stack) Whether a mark has an encoding with stacking.
helper(mark_with_stack,M) :-
    entity(encoding,M,E),
    attribute((encoding,stack),E,_).

% @helper(mark_scale) Whether a mark has a scale.
helper((mark,scale),M,S) :-
    entity(mark,V,M),
    entity(scale,V,S).
helper((mark,scale),M,S) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,S).

% @helper(mark_scale_channel) Whether a mark has a scale type for a channel.
helper(mark_scale_channel,M,T,C) :-
    helper((mark,scale),M,S),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,T).

% @helper(mark_encoding_scale) Link mark, encoding, and scale togther.
helper(mark_encoding_scale,M,E,S) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    helper((mark,scale),M,S),
    attribute((scale,channel),S,C).

% @helper(encoding_type) Whether an encoding has a channel for a scale type.
helper((encoding,scale_type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    helper(mark_scale_channel,M,T,C).

% @helper(mark_channel_field) Whether a mark has an encoding for a field and a channel.
helper(mark_channel_field,M,C,F) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,F).

% % @helper(mark_channel_scale) whether a mark has a scale type for a channel(with or without binned encoding).
% helper(mark_channel_scale,M,T,C,B) :-
%     entity(encoding,M,E),
%     attribute((encoding,channel),E,C),
%     helper(mark_scale_channel,M,T,C),
%     attribute((encoding,binning),E,B).
% helper(mark_channel_scale,M,T,C) :-
%     entity(encoding,M,E),
%     attribute((encoding,channel),E,C),
%     helper(mark_scale_channel,M,T,C),
%     not attribute((encoding,binning),E,_).

% @helper(mark_channel_discrete_or_binned) Whether a mark has a discrete scale or binned encoding for a channel.
helper(mark_channel_discrete_or_binned,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    helper(mark_scale_channel,M,T,C),
    domain(discrete_scale,T).
helper(mark_channel_discrete_or_binned,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,binning),E,_).

% @helper(mark_encoding_discrete_or_binned) Whether a mark has a discrete scale or binned encoding for an encoding.
helper(mark_encoding_discrete_or_binned,M,E) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    helper(mark_scale_channel,M,T,C),
    domain(discrete_scale,T).
helper(mark_encoding_discrete_or_binned,M,E) :-
    entity(encoding,M,E),
    attribute((encoding,binning),E,_).

% @helper(mark_encoding_cont) Whether a mark has a continuous for an encoding.
helper(mark_encoding_cont,M,E) :-
    entity(encoding,M,E),
    not helper(mark_encoding_discrete_or_binned,M,E).

% @helper(mark_channel_cont) Whether a mark has a continuous scale for a channel.
helper(mark_channel_cont,M,C) :-
    helper((mark,channel),M,C),
    not helper(mark_channel_discrete_or_binned,M,C).

% @helper(encoding_cardinality) The cardinality of an encoding.
helper(encoding_cardinality,E,N) :-
    attribute((field,unique),F,N),
    attribute((encoding,field),E,F),
    not attribute((encoding,binning),E,_).
helper(encoding_cardinality,E,N) :-
    attribute((encoding,binning),E,N).

% @helper(discrete_cardinality) The cardinality of a discrete encoding.
helper(discrete_cardinality,M,E,N) :-
    helper(encoding_cardinality,E,N),
    helper(mark_encoding_discrete_or_binned,M,E).

% @helper(facet_cardinality,Fa,N) The cardinality of a facet.
helper(facet_cardinality,Fa,N) :-
    attribute((field,unique),Fi,N),
    attribute((facet,field),Fa,Fi),
    not attribute((facet,binning),Fa,_).
helper(facet_cardinality,Fa,N) :-
    attribute((facet,binning),Fa,N).

% @helper(is_c_c) Continuous by continuous.
helper(is_c_c,M) :-
    entity(mark,_,M),
    helper((mark,channel),M,x),
    helper((mark,channel),M,y),
    not helper(mark_channel_discrete_or_binned,M,x),
    not helper(mark_channel_discrete_or_binned,M,y).

% @helper(is_c_d) Continuous by discrete (or only one continuous).
helper(is_c_d,M) :-
    entity(mark,_,M),
    helper(mark_channel_cont,M,x),
    not helper(mark_channel_cont,M,y).
helper(is_c_d,M) :-
    entity(mark,_,M),
    not helper(mark_channel_cont,M,x),
    helper(mark_channel_cont,M,y).

% @helper(is_d_d) Discrete by discrete.
helper(is_d_d,M) :-
    helper((mark,channel),M,x),
    helper((mark,channel),M,y),
    helper(mark_channel_discrete_or_binned,M,x),
    helper(mark_channel_discrete_or_binned,M,y).
helper(is_d_d,M) :-
    helper((mark,channel),M,x),
    helper(mark_channel_discrete_or_binned,M,x),
    not helper((mark,channel),M,y).
helper(is_d_d,M) :-
    helper((mark,channel),M,y),
    helper(mark_channel_discrete_or_binned,M,y),
    not helper((mark,channel),M,x).

% @helper(non_pos_unaggregated) Non-positional channels are unaggregated.
helper(non_pos_unaggregated,M) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    domain(non_positional,C),
    not attribute((encoding,aggregate),E,_).

% @helper(no_overlap) The continuous variable is a measure (it is aggregated) and all other non-positional channels are aggregated, or we use stack.
helper(no_overlap,M) :-
    helper(is_c_d,M),
    helper(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,(x;y)),
    attribute((encoding,aggregate),E,_),
    not helper(non_pos_unaggregated,M).
helper(no_overlap,M) :-
    helper(is_c_d,M),
    entity(encoding,M,E),
    attribute((encoding,stack),E,_).
helper(no_overlap,M) :-
    helper(is_c_d,M),
    attribute(number_rows,root,N),
    helper(discrete_size,M,N).
helper(no_overlap,M) :-
    helper(is_d_d,M),
    helper((mark,channel),M,C),
    domain(non_positional,C),
    not helper(non_pos_unaggregated,M).
helper(no_overlap,M) :-
    helper(is_d_d,M),
    attribute(number_rows,root,N1),
    helper(discrete_size,M,N2),
    N1 <= N2.

% @helper(overlap) We definitely overlap if the data size > discrete size.
helper(overlap,M) :-
    helper(is_c_d,M),
    not helper(no_overlap,M),
    attribute(number_rows,root,N1),
    helper(discrete_size,M,N2),
    N1 > N2.
helper(overlap,M) :-
    entity(mark,V,M),
    helper(is_d_d,M),
    not helper(no_overlap,M),
    not entity(facet,V,_),
    attribute(number_rows,root,N1),
    helper(discrete_size,M,N2),
    N1 > N2.

% @helper(discrete_size) The size of the discrete positional encoding.
helper(discrete_size,M,N) :-
    helper(is_c_d,M),
    helper(x_cardinality,M,N).
helper(discrete_size,M,N) :-
    helper(is_c_d,M),
    helper(y_cardinality,M,N).
helper(discrete_size,M,1) :-
    helper(is_c_d,M),
    helper(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,x),
    not helper((mark,channel),M,y).
helper(discrete_size,M,1) :-
    helper(is_c_d,M),
    helper(mark_encoding_cont,M,E),
    attribute((encoding,channel),E,y),
    not helper((mark,channel),M,x).
helper(discrete_size,M,N) :-
    helper(is_d_d,M),
    helper(x_cardinality,M,NX),
    helper(y_cardinality,M,NY),
    N = NX*NY.

% @helper(x_cardinality) Cardinality of discrete x. Helps to go from quadratic to linear number of grounding.
helper(x_cardinality,M,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,x),
    helper(discrete_cardinality,M,E,N).
helper(x_cardinality,M,1) :-
    entity(mark,_,M),
    not helper((mark,channel),M,x).

% @helper(y_cardinality) Cardinality of discrete x. Helps to go from quadratic to linear number of grounding.
helper(y_cardinality,M,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,y),
    helper(discrete_cardinality,M,E,N).
helper(y_cardinality,M,1) :-
    entity(mark,_,M),
    not helper((mark,channel),M,y).
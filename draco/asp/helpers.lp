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

% @helper(encoding_cardinality,E,N) The cardinality of an encoding.
attribute(encoding_cardinality,E,N) :-
    attribute((field,unique),F,N),
    attribute((encoding,field),E,F),
    not attribute((encoding,binning),E,_).
attribute(encoding_cardinality,E,N) :-
    attribute((encoding,binning),E,N).

% @helper(field_scale,F,T) The scale type for a field.
attribute(field_scale,F,T): :-
    attribute(mark_channel_field,M,C,F),
    attribute(mark_scale_channel,M,T,C).

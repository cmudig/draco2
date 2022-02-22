% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute((mark,channel),M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_scale_channel) Whether a mark has a scale type for a channel.
attribute(mark_scale_channel,M,T,C) :-
    entity(mark,V,M),
    entity(scale,V,S),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,T).
attribute(mark_scale_channel,M,T,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,S),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,T).

% @helper(encoding_type) whether an encoding has a channel for a scale type.
attribute((encoding,scale_type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,T,C).

% @helper(mark_channel_field) Whether a mark has an encoding for a field  and a channel.
attribute(mark_channel_field,M,C,F) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,F).

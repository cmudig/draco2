% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute(mark_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_scale_channel) Whether a mark has a scale for a channel.
attribute(mark_scale_channel,M,S,C) :-
    entity(mark,V,M),
    entity(scale,V,S),
    attribute((scale,channel),S,C).
attribute(mark_scale_channel,M,S,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,S),
    attribute((scale,channel),S,C).

% @helper(encoding_type)
attribute((encoding,scale_type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,T).

% ====== Helpers ======

% @helper(has_channel) Whether a mark has an encoding for a channel.
attribute(has_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(has_stack) Whether a mark has an encoding with stacking.
attribute(has_stack,M) :-
    entity(encoding,M,E),
    attribute((encoding,stack),E,_).

% @helper(has_discrete_color) Whether a mark has discrete color encoding
attribute(has_discrete_color,M) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,color),
    attribute((scale,channel),S,color),
    attribute((scale,type),S,ordinal).

% @helper(discrete) Whether an encoding is discrete.
attribute(discrete,E) :-
    entity(encoding,_,E),
    attribute((encoding,channel),E,C),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,(ordinal;nominal)).

attribute(discrete,E) :-
    attribute((encoding,binning),E,_).

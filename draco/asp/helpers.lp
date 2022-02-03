% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute(mark_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_scale_channel) Whether a mark has an scale for a channel.
attribute(mark_scale_channel,M,S,C) :-
    entity(mark,V,M),
    entity(scale,V,S),
    attribute((scale,channel),S,C).
attribute(mark_scale_channel,M,S,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,S),
    attribute((scale,channel),S,C).

% @helper(extent) extent of a field.
attribute(extent,F,MIN,MAX) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX).

% @helper(discrete) Whether the channel is discrete.
attribute(discrete,M,C) :-
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,(ordinal;categorical)).

% @helper(continuous) Whether the channel is continuous.
attribute(continuous,M,C) :-
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,(linear;log)).

% @helper(encoding_type)
attribute((encoding,scale_type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,T).

% % @helper(channel_type)
% attribute(channel_type,V,T) :-

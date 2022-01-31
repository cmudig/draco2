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

% @helper(check_field_type) Whether a field is of type T.
attribute(field_type,N,T) :-
    attribute((field,name),F,N),
    attribute((field,type),F,T).

% @helper(check_scale_type) Whether a scale is of type T.
attribute(scale_type,M,C,T) :-
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,T).

% @helper(check_channel_field) Whether the channel is referring to the field.
attribute(channel_field,M,C,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,N).

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
attribute((encoding,type),E,T) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute(mark_scale_channel,M,S,C),
    attribute((scale,type),S,T).

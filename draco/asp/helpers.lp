% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute(mark_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(mark_scale_channel) Whether a mark has an scale for a channel.
attribute(mark_scale_channel,M,E,C) :-
    entity(mark,V,M),
    entity(scale,V,E),
    attribute((scale,channel),E,C).
attribute(mark_scale_channel,M,E,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,E),
    attribute((scale,channel),E,C).

% @helper(check_field_type) Whether a field is of type T.
attribute(field_type,N,T) :-
    attribute((field,name),F,N),
    attribute((field,type),F,T).

% @helper(check_scale_type) Whether a scale is of type T.
attribute(scale_type,M,C,T) :-
    attribute(mark_scale_channel,M,E,C),
    attribute((scale,type),E,T).

% @helper(check_channel_field) Whether the channel is referring to the field.
attribute(channel_field,M,C,N) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,N).

% @helper(extent) extent of a field.
attribute(extent,N,MIN,MAX) :-
    attribute((field,min),N,MIN),
    attribute((field,max),N,MAX).

% @helper(discrete) Whether the channel is discrete.
attribute(discrete,M,C) :-
    attribute(mark_scale_channel,M,E,C),
    attribute((scale,type),E,(ordinal;categorical)).

% @helper(continuous) Whether the channel is continuous.
attribute(continuous,M,C) :-
    attribute(mark_scale_channel,M,E,C),
    attribute((scale,type),E,(linear;log)).

% @helper(mark_x_y_channels) whether a mark has both x and y channels.
attribute(mark_x_y_channels,M) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,x),
    attribute((encoding,channel),E2,y).

% @helper(mark_cont_channel) Whether a mark has a continuous channel C.
attribute(mark_cont_channel,M,C) :-
    attribute(mark_channel,M,C),
    attribute(continuous,M,C).

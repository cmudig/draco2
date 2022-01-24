% ====== Helpers ======

% @helper(has_channel) Whether a mark has an encoding for a channel.
attribute(has_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

% @helper(check_field_type) Whether a field is of type T.
attribute(check_field_type,F,T) :-
    attribute((field,name),E,F),
    attribute((field,type),E,T).

% @helper(check_scale_type) Whether a scale is of type T.
attribute(check_scale_type,C,T) :-
    attribute((scale,channel),E,C),
    attribute((scale,type),E,T).
attribute(check_scale_type,M,C,T) :-
    entity(mark,V,M),
    entity(scale,V,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,T).
attribute(check_scale_type,M,C,T) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,T).

% @helper(check_channel_field) Whether the channel is referring to the field.
attribute(check_channel_field,M,C,F) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,field),E,F).

% @helper(extent) extent of a field.
attribute(extent,F,MIN,MAX) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX).

% @helper(discrete) Whether the channel is discrete.
attribute(discrete,M,C) :-
    entity(mark,V,M),
    entity(scale,V,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,(ordinal;categorical)).
attribute(continuous,M,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,(ordinal;categorical)).

% @helper(continuous) Whether the channel is continuous.
attribute(continuous,M,C) :-
    entity(mark,V,M),
    entity(scale,V,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,(linear;log)).
attribute(continuous,M,C) :-
    entity(view,R,V),
    entity(mark,V,M),
    entity(scale,R,E),
    attribute((scale,channel),E,C),
    attribute((scale,type),E,(linear;log)).

% @helper(has_x_y_channels) whether a mark has both x and y channels.
attribute(has_x_y_channels,M) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,x),
    attribute((encoding,channel),E2,y).

% @helper(has_cont_channel) Whether a mark has a continuous channel C.
attribute(has_cont_channel,M,C) :-
    attribute(has_channel,M,C),
    attribute(continuous,M,C).

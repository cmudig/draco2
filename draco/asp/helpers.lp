% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute((mark,channel),M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

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

% @helper(mark_channel_scale_not_binned) Whether a mark has a scale type for a channel that is not binned.
attribute(mark_channel_scale_not_binned,M,T,C) :-
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
    attribute(mark_scale_channel,M,T,C),
    attribute((encoding,binning),E,_).


% ====== Helpers ======

% @helper(has_channel) Whether a mark has an encoding for a channel.
attribute(has_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).

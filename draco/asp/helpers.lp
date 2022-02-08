% ====== Helpers ======

% @helper(mark_channel) Whether a mark has an encoding for a channel.
attribute(mark_channel,M,C) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C).
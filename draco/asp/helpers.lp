% ====== Helpers ======


% @helper(has_channel) Whether a mark has an encoding for a channel.
attribute(has_channel,M,C) :-
    property(encoding,M,E),
    attribute(channel,E,C).

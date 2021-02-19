% ====== Hard constraints ======

% @hard(text_mark_without_text_channel) Text mark requires text encoding.
attribute(has_channel,M,C) :-
    property(encoding,M,E),
    attribute(channel,E,C).

violoation(text_mark_without_text_channel) :-
    attribute(mark_type,M,text),
    not attribute(has_channel,M,text).

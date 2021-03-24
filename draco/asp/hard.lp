% ====== Hard constraints ======

% @hard(text_mark_without_text_channel) Text mark requires text encoding.
violation(text_mark_without_text_channel) :-
    attribute(mark_type,M,text),
    not attribute(has_channel,M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    not attribute(mark_type,M,text),
    attribute(has_channel,M,text).

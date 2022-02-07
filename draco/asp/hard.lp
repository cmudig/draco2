% ====== Hard constraints ======

% @hard(text_mark_without_text_channel) Text mark requires text encoding.
violation(text_mark_without_text_channel) :-
    attribute((mark,type),M,text),
    not attribute(mark_channel,M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    attribute(mark_channel,M,text),
    not attribute((mark,type),M,text).

% @hard(bin_and_aggregate) Cannot bin and aggregate.
violation(bin_and_aggregate) :-
    attribute((encoding,binning),E,_),
    attribute((encoding,aggregate),E,_).

% === Across encodings and between encodings and marks ===

% @hard(repeat_channel) Cannot use single channels twice for the same mark.
violation(repeat_channel) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 != E2.

% @hard(no_encodings) There has to be at least one encoding for every mark.
violation(no_encodings) :-
    entity(mark,_,M),
    not entity(encoding,M,_).

% @hard(encoding_no_field_and_not_count) All encodings (if they have a channel) require field except if we have a count aggregate.
violation(encoding_no_field_and_not_count) :-
    entity(encoding,_,E),
    not attribute((encoding,field),E,_),
    not attribute((encoding,aggregate),E,count).

% @hard(count_with_field) Count should not have a field. Having a field doesn't make a difference.
violation(count_with_field) :-
    attribute((encoding,aggregate),E,count),
    attribute((encoding,field),E,_).

% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    attribute((mark,type),M,(point;tick;bar)),
    not attribute(mark_channel,M,x),
    not attribute(mark_channel,M,y).

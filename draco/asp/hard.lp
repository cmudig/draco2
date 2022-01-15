% ====== Hard constraints ======

% @hard(text_mark_without_text_channel) Text mark requires text encoding.
violation(text_mark_without_text_channel) :-
    attribute((mark,type),M,text),
    not attribute(has_channel,M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    not attribute((mark,type),M,text),
    attribute(has_channel,M,text).

% @hard(bin_and_aggregate) Cannot bin and aggregate.
violation(bin_and_aggregate) :-
    attribute((encoding,binning),E,_),
    attribute((encoding,aggregate),E,_).

% @hard(no_encodings) There has to be at least one encoding.
violation(no_encodings) :- not entity(encoding,_,_).

% @hard(repeat_channel) Cannot use single channels twice.
violation(repeat_channel) :-
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 != E2.

% @hard(row_no_y) Don't use row without y. Just using y is simpler.
violation(row_no_y) :-
    attribute((encoding,channel),_,row),
    not attribute((encoding,channel),_,y).

% @hard(encoding_no_field_and_not_count) All encodings (if they have a channel) require field except if we have a count aggregate.
violation(encoding_no_field_and_not_count) :-
    not attribute((encoding,field),E,_),
    not attribute((encoding,aggregate),E,count),
    entity(encoding,_,E).

% @hard(count_with_field) Count should not have a field. Having a field doesn't make a difference.
violation(count_with_field) :-
    attribute((encoding,aggregate),E,count),
    attribute((encoding,field),E,_).


% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    entity(encoding,_,E),
    attribute((mark,type),E,(point;tick;bar)),
    not attribute((encoding,channel),E,x),
    not attribute((encoding,channel),E,y).
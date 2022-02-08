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

% @hard(no_encodings) There has to be at least one encoding for every mark.
violation(no_encodings) :-
    entity(mark,_,M),
    not entity(encoding,M,_).

% @hard(repeat_channel) Cannot use single channels twice for the same mark.
violation(repeat_channel) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 != E2.

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

% @hard(invalid_bin) Check bin type.
violation(invalid_bin) :-
    attribute((encoding,binning),_,B),
    not B >= 0.

% @hard(invalid_num_rows) Num_rows has to be larger than 0.
violation(invalid_num_rows) :-
    attribute(number_rows,root,R),
    R <= 0.

% @hard(invalid_unique) The number of unique values has to be larger than 0.
violation(invalid_unique) :-
    attribute((field,unique),_,U),
    U <= 0.

% @hard(invalid_extent_non_number_min) Extent only allowed for numbers (for now).
violation(invalid_extent_non_number_min) :-
    attribute((field,min),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_extent_non_number_max) Extent only allowed for numbers (for now).
violation(invalid_extent_non_number_max) :-
    attribute((field,max),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_non_number_std) Std only allowed for numbers (for now).
violation(invalid_non_number_std) :-
    attribute((field,std),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_std) Std has to be larger or equal to 0.
violation(invalid_std) :-
    attribute((field,std),_,S),
    S < 0.

% @hard(invalid_extent_order) Order has to be correct.
violation(invalid_extent_order) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX),
    MIN > MAX.

% @hard(invalid_non_string_freq) Frequency for strings only.
violation(invalid_non_string_freq) :-
    attribute((field,freq),F,_),
    not attribute((field,type),F,string).

% @hard(encoding_field_same_name) The name of a field cannot be the name of an encoding. This is to prevent errors coming from the shortcuts in define.lp.
violation(encoding_field_same_name) :-
    attribute((field,name),0,F),
    domain(channel,F).
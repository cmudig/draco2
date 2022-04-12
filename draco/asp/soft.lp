% ====== Preferences ======

% @soft(aggregate) Prefer to use raw (no aggregate).
preference(aggregate,E) :-
    attribute((encoding,aggregate),E,_).

% @soft(bin) Prefer to not bin.
preference(bin,E) :-
    attribute((encoding,binning),E,_).

% @soft(bin_high) Prefer binning with at most 12 buckets.
preference(bin_high,E) :-
    attribute((encoding,binning),E,B), B > 12.

% @soft(bin_low) Prefer binning with more than 7 buckets.
preference(bin_low,E) :-
    attribute((encoding,binning),E,B), B <= 7.

% @soft(encoding) Prefer to use fewer encodings.
preference(encoding,E) :-
    entity(encoding,_,E).

% @soft(encoding_field) Prefer to use fewer encodings with fields (count does not have a field).
preference(encoding_field,E) :-
    attribute((encoding,field),E,_).

% @soft(same_field) Prefer not to use the same field twice for the same mark.
preference(same_field,F) :-
    entity(field,_,F),
    entity(mark,_,M),
    { entity(encoding,M,E): attribute((encoding,field),E,F) } = 2.

% @soft(type_linear) Prefer linear=log>ordinal>categorical
preference(type_linear,E) :-
    attribute((encoding,scale_type),E,linear).

% @soft(type_log) Prefer linear=log>ordinal>categorical
preference(type_log,E) :-
    attribute((encoding,scale_type),E,log).

% @soft(type_ordinal) Prefer linear=log>ordinal>categorical
preference(type_ordinal,E) :-
    attribute((encoding,scale_type),E,ordinal).

% @soft(type_categorical) Prefer linear=log>ordinal>categorical
preference(type_categorical,E) :-
    attribute((encoding,scale_type),E,categorical).

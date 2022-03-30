% ====== Preferences ======
% @soft(aggregate) Prefer to use raw (no aggregate).
preference(aggregate,E) :-
    attribute((encoding,aggregate),E,_).
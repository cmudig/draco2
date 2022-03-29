% ====== Preferences ======
% @soft(aggregate) Prefer to use raw (no aggregate).
violation(aggregate,E) :-
    attribute((encoding,aggregate),E,_).
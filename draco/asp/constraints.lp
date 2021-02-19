% ====== Constraints ======

% @definition(invalid_domain) Only valid domain values are allowed.
violoation(invalid_domain) :- attribute(P,_,V), domain(P,_), not domain(P,V).

% @definition(duplicate_attribute) Only valid domain values are allowed.
violoation(duplicate_attribute) :- attribute(P,O,V1), attribute(P,O,V2), V1!=V2.

% no violations allowed
:- violoation(_).

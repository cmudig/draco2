% ====== Constraints ======

% @definition(invalid_domain) Only valid domain values are allowed.
violoation(invalid_domain) :- attribute(X,_,V), domain(X,_), not domain(X,V).

% no violations allowed
:- violoation(_).

% ====== Constraints ======

% @definition(invalid_domain) Only valid domain values are allowed.
violation(invalid_domain) :- attribute(P,_,V), domain(P,_), not domain(P,V).

% @definition(duplicate_attribute) Only valid domain values are allowed.
violation(duplicate_attribute) :- attribute(P,O,V1), attribute(P,O,V2), V1!=V2.

% @definition(valid_fields) Only allow fields that have been defined.
violation(existing_field) :- attribute((encoding,field),_,F), not attribute((field,name),_,F).

% @definition(attribute_property) The type of an attribute path should link to the correct property.
violation(attribute_property) :- attribute((P,_),E,_), property(_,_,E), not property(P,_,E).

% @definition(violation) No violations allowed.
:- violation(_).

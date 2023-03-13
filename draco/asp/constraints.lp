% ====== Constraints ======

% @definition(invalid_domain) Only valid domain values are allowed.
violation(invalid_domain) :- attribute(P,_,V), domain(P,_), not domain(P,V).

% @definition(duplicate_attribute) Do not define the same attribute twice.
violation(duplicate_attribute) :- attribute(P,O,V1), attribute(P,O,V2), domain(P,_), V1<V2.

% @definition(duplicate_field_name) Do not allow same field names.
violation(duplicate_field_name) :- attribute((field,name),F1,N), attribute((field,name),F2,N), F1<F2.

% @definition(valid_fields) Only allow fields that have been defined.
violation(existing_field) :- attribute(((encoding;facet),field),_,N), not attribute((field,name),_,N).

% @definition(attribute_entity) The type of an attribute path should link to the correct entity.
violation(attribute_entity) :- attribute((P,_),E,_), entity(_,_,E), not entity(P,_,E).

% @definition(violation) No violations allowed.
:- violation(_).

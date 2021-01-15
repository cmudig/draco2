% ====== Definitions of valid function domains ======

#script (python)

from clingo import Function

def args(term):
    return term.arguments

def name(term):
    return Function(term.name)

#end.

domain(R,Elem) :-
    definition(R,C),
    Elem = @args(C),
    pool = @name(C).

#show domain/2.

% @definition(mark_type) Types of marks to encode data.
definition(mark_type,pool(point,bar,line,area,text,tick,rect)).

% @definition(field_type) Basic types of the data.
definition(field_type,pool(string,number,boolean,datetime)).

% @definition(aggregate) Supported aggregation functions.
definition(aggregate_op,pool(count,mean,median,min,max,stdev,sum)).
definition(summative_aggregate_op,pool(count,sum)).

% @definition(binning) Numbers of bins that can be recommended, any natural number is allowed.
definition(binning,pool(10,25,200)).

% @definition(channel) Encoding channels.
definition(single_channel,pool(x,y,color,size,shape,text,row,column)).
domain(multi_channel,detail).
domain(channel,C) :- domain(single_channel,C).
domain(channel,C) :- domain(multi_channel,C).
definition(non_positional,pool(color,size,shape,text,detail)).

% @definition(task) Possible tasks.
definition(task,pool(value,summary)).

% @definition(stack) Possible stacking methods.
definition(stack,pool(zero,normalize)).

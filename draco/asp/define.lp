% ====== Definitions ======

% @definition(marktype) Types of marks to encode data.
marktype(point;bar;line;area;text;tick;rect).

% @definition(field_type) Basic types of the data.
fieldType(string;number;boolean;datetime).

% @definition(aggregate) Supported aggregation functions.
aggregate_op(count;mean;median;min;max;stdev;sum).
summative_aggregate_op(count;sum).

% @definition(binning) Numbers of bins that can be recommended; any natural number is allowed.
binning(10;25;200).

% @definition(channel) Encoding channels.
single_channel(x;y;color;size;shape;text;row;column).
multi_channel(detail).
channel(C) :- single_channel(C).
channel(C) :- multi_channel(C).
non_positional(color;size;shape;text;detail).

% @definition(task) Possible tasks.
task(value;summary).

% @definition(stack) Possible stacking methods.
stack(zero;normalize).

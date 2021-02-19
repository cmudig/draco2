# Schema Description

The schema describes what we know about the dataset and the fields in the data. Besides general statistics about the whole dataset, the schema also has information about field types and field statistics.

## Dataset Properties

`number_rows`
: The number of rows in the dataset. Draco can use this fact about the data to recommend chart design that scale to the size of the dataset.

## Field Properties

Draco can use information about the field type and field statistics. Each field property is associated with a field. The facts therefore have the form of e.g. `attribute(data_type,foo,number).` (read as _the type of the foo field is number_). For each field, there should be a property fact `property` that tells Draco that the field exists on the root object (e.g. `property(field,root,foo).`).

`data_type`
: The type of the data in the column for this field. One of `number`, `string`, `boolean`, or `datetime`.

`unique`
: The number of unique values.

`min`
: The minimum value. Only used for numbers.

`max`
: The maximum value. Only used for numbers.

`std`
: The standard deviation. Only used for numbers.

`freq`
: The frequency of the most common value. Only used for strings.

## Example

```prolog
fact(number_rows,root,42).

property(field,root,date).
attribute(data_type,date,datetime).
attribute(unique,date,1461).

property(field,root,precipitation).
attribute(data_type,precipitation,number).
attribute(unique,precipitation,111).
attribute(min,precipitation,0).
attribute(max,precipitation,55).
attribute(std,precipitation,6).

property(field,root,weather).
attribute(data_type,weather,string).
attribute(unique,weather,5).
attribute(freq,weather,714).
```

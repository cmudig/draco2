# Schema Description

The schema describes what we know about the dataset and the fields in the data. Besides general statistics about the whole dataset, the schema also has information about field types and field statistics.

## Dataset Properties

`numberRows`
: The number of rows in the dataset. Draco can use this fact about the data to recommend chart design that scale to the size of the dataset.

## Field Properties

Draco can use information about the field type and field statistics. Each field property is associated with a field. The facts therefore have the form of e.g. `fact(dataType,foo,number).` (read as _the type of the foo field is number_). For each field, there should be a fact `field` that tells Draco that the field exists (e.g. `fact(field,foo).`).

`dataType`
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
fact(numberRows,42).

fact(field,date).
fact(dataType,date,datetime).
fact(unique,date,1461).

fact(field,precipitation).
fact(dataType,precipitation,number).
fact(unique,precipitation,111).
fact(min,precipitation,0).
fact(max,precipitation,55).
fact(std,precipitation,6).

fact(field,weather).
fact(dataType,weather,string).
fact(unique,weather,5).
fact(freq,weather,714).
```

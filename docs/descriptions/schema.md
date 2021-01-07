# Schema Description

The schema describes what we know about the dataset and the fields in the data. Besides general statistics about the whole dataset, the schema also has information about field types and field statistics.

## General Dataset Properties

`numberRows`
: The number of rows in the dataset. Draco can use this fact about the data to recommend chart design that scale to the size of the dataset.

## Field Properties

Draco can use knowledge about the field type and field statistics.

`dataType`
: The type of the data in the column for this field. One of `number`, `string`, `boolean`, or `date`.

`unique`
: The number of unique values.

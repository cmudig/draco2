# Data and Schema

In Draco, you can describe what you know about the dataset and the fields in the data. There can be only one dataset in a Draco program.

Besides general statistics about the whole dataset, the schema has information about field types and field statistics.

You can use Draco's [data schema API](../api/schema.ipynb) to generate a schema description from a file or Pandas dataframe.

## Dataset Properties

General properties of the dataset that are not specific to a field are properties of the root.

`number_rows`
: The number of rows in the dataset. Draco can use this fact about the data to recommend chart design that scale to the size of the dataset.

## Field Properties

Draco can use information about the field type and field statistics. Each field property is associated with a field. The facts therefore have the form of e.g. `attribute((field,type),foo,number).` (read as _the type of the foo field is number_). For each field, there should be a property fact `property` that tells Draco that the field exists on the root object (e.g. `property(field,root,foo).`).

`(field,type)`
: The type of the data in the column for this field. One of `number`, `string`, `boolean`, or `datetime`.

`(field,unique)`
: The number of unique values.

`(field,min)`
: The minimum value. Only used for numbers.

`(field,max)`
: The maximum value. Only used for numbers.

`(field,std)`
: The standard deviation. Only used for numbers.

`(field,freq)`
: The frequency of the most common value. Only used for strings.

## Example

```prolog
attribute(number_rows,root,42).

property(field,root,date).
attribute((field,type),date,datetime).
attribute((field,unique),date,1461).

property(field,root,precipitation).
attribute((field,type),precipitation,number).
attribute((field,unique),precipitation,111).
attribute((field,min),precipitation,0).
attribute((field,max),precipitation,55).
attribute((field,std),precipitation,6).

property(field,root,weather).
attribute((field,type),weather,string).
attribute((field,unique),weather,5).
attribute((field,freq),weather,714).
```

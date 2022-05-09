# Data and Schema

In Draco, you can describe what you know about the dataset and the fields in the data. There can be only one dataset in a Draco program.

Besides general statistics about the whole dataset, the schema has information about field types and field statistics.

You can use Draco's [data schema API](../api/schema.ipynb) to generate a schema description from a file or Pandas dataframe.

## Dataset Properties

General properties of the dataset that are not specific to a field are properties of the root.

`number_rows`
: The number of rows in the dataset. Draco can use this fact about the data to recommend chart design that scale to the size of the dataset.

## Field Properties

Draco can use information about the field type and field statistics. Each field entity is associated with a field. The facts therefore have the form of e.g. `attribute((field,type),foo,number).` (read as _the type of the foo field is number_). For each field, there should be a entity fact `entity` that tells Draco that the field exists on the root (e.g. `entity(field,root,foo).`).

`(field,name)`
: The name of the field.

`(field,type)`
: The type of the data in the column for this field. One of `number`, `string`, `boolean`, or `datetime`.

`(field,unique)`
: The number of unique values.

`(field,entropy)`
: The entropy of the field. (To save a more accurate value, this field entropy value is 1000 times of the actual entropy).

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

entity(field,root,f1).
attribute((field,name),f1,date).
attribute((field,type),f1,datetime).
attribute((field,unique),f1,1461).
attribute((field,entropy),f1,7287).

entity(field,root,f2).
attribute((field,name),f2,precipitation).
attribute((field,type),f2,number).
attribute((field,unique),f2,111).
attribute((field,min),f2,0).
attribute((field,max),f2,55).
attribute((field,std),f2,6).
attribute((field,entropy),f1,2422).

entity(field,root,f3).
attribute((field,name),f3,weather).
attribute((field,type),f3,string).
attribute((field,unique),f3,5).
attribute((field,freq),f3,714).
attribute((field,entropy),f1,1201).
```

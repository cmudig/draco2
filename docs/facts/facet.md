# Facets

With the facet operator, we can partition a dataset by a field and create a view for each field. The resulting chart is
often called a small multiples chart.

## Facet Properties

`(facet,channel)` : The facet channel. Can be one of `col` and `row`.

`(facet,field)` : The facet field. Note that the field should refers to field `name` rather than the field `entity` id.
Although we specify the name and the id in the same way in the following examples, they can be different.

`(facet,binning)` : Binning a numeric field for faceting.

## Example

```prolog
entity(field,root,condition).
attribute((field,name),condition,condition).
attribute((field,type),condition,string).

entity(view,root,v).

entity(facet,v,f).
attribute((facet,channel),f,col).
attribute((facet,field),f,condition).
```

```prolog
entity(field,root,temperature).
attribute((field,name),temperature,temperature).
attribute((field,type),temperature,number).

entity(view,root,v).

entity(facet,v,f).
attribute((facet,channel),f,col).
attribute((facet,field),f,temperature).
attribute((facet,binning),f,10).
```

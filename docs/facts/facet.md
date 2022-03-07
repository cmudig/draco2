# Facets

The facet option can expand current view into horizontal or vertical small multiples.

## Facet Properties

`(facet,channel)`
: The facet channel. Can be one of `col`, and `row`.

`(facet,channel)`
: The facet field.

`(facet,binning)`
: Binning a quantitative field for faceting.

## Example

```prolog
entity(facet,root,f).
attribute((facet,channel),f,col).
attribute((facet,field),f,condition).
```

```prolog
entity(facet,root,f).
attribute((facet,channel),f,col).
attribute((facet,field),f,temperature).
attribute((facet,binning),f,10).
```

# Scales

Scales map abstract values such as time or temperature to a visual values such as x- or y-position or color.

A scale is primarily defined by its input **domain** and output **range**.

Scales with continuous domain and range are known as quantitative scales. The scale can be `linear`, `log`arithmic, etc.

Scales with a discrete domain of categorical values that map to a continuous range are known as `ordinal` scales. Discrete color scales can either be `ordinal` when the data are ordered and `categorical` otherwise.

## Scale Properties

`(scale,channel)`
: The scale channel. One of `x`, `y`, `color`, `size`, `shape`, or `text`.

`(scale,type)`
: The scale type. One of `linear`, `log`, `ordinal`, or `categorical`.

## Example

```prolog
attribute((scale,channel),1,x).
attribute((scale,type),1,linear).
```

```prolog
attribute((scale,channel),1,color).
attribute((scale,type),1,categorical).
```

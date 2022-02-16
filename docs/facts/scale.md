# Scales

Scales map abstract values such as time or temperature to a visual values such as x- or y-position or color.

A scale is primarily defined by its input **domain** and output **range**.

Scales with continuous domain and range are called quantitative scales. The scale can be `linear`, `log`arithmic, etc.

Scales with a discrete domain of categorical values that map to a continuous range are called `ordinal` scales. Discrete color scales can either be `ordinal` when the data are ordered and `categorical` otherwise.

## Scale Properties

`(scale,channel)`
: The scale channel. One of `x`, `y`, `color`, `size`, `shape`, or `text`. Same as the [encoding channel](encoding.md).

`(scale,type)`
: The scale type. One of `linear`, `log`, `ordinal`, or `categorical`.

## Example

```prolog
attribute((scale,channel),s,x).
attribute((scale,type),s,linear).
```

```prolog
attribute((scale,channel),s,color).
attribute((scale,type),s,categorical).
```

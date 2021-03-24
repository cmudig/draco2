# Marks

The mark represents the graphical mark of the visualization. Draco uses an encoding based on the Grammar of Graphics (GoG) {cite}`wilkinson2012grammar`. In the GoG, marks are described as Geometric objects ("geoms" for short). We use the term mark as that's the term Vega-Lite {cite}`satyanarayan2016vega` uses.

If you define multiple marks or a view has multiple marks, Draco assumes that the marks are layered (i.e. they are in the same view space in the chart).

## Mark Properties

`(mark,type)`
: The mark type. One of `point`, `bar`, `line`, `area`, `text`, `tick`, or `rect`.

## Example

```prolog
attribute((mark,type),1,tick).
```

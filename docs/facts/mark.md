# Mark Description

The mark represents the graphical mark of the visualization. Draco uses an encoding based on the Grammar of Graphics (GoG) {cite}`wilkinson2012grammar`. In the GoG, marks are described as Geometric objects ("geoms" for short). We use the term mark as that's the term Vega-Lite {cite}`satyanarayan2016vega` uses.

## Mark Properties

`(mark,type)`
: The mark type. One of `point`, `bar`, `line`, `area`, `text`, `tick`, or `rect`.

## Example

```prolog
attribute((mark,type),1,tick).
```

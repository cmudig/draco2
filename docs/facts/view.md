# Views

A view can group marks and scales together. You need to define a view before you add any marks.

If a view has multiple marks, Draco assumes that the marks are layered (i.e. they are in the same view space in the chart).

## View Properties

`(view,coordinates)`
: The coordinates system of the view. Can be one of `cartesian`, or `polar`.

## Example

Here, we define a single view `v` of a tick plot.

```prolog
entity(view,root,v).
attribute((view,coordinates),v,cartesian).

entity(mark,v,m).
attribute((mark,type),m,tick).
entity(encoding,m,e1).
attribute((encoding,channel),e1,x).
attribute((encoding,field),e1,temperature).

entity(scale,v,4).
attribute((scale,channel),4,x).
attribute((scale,type),4,linear).
```

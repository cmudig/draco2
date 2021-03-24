# View Description

A view can group marks and scales together. You don't always need a view. For example, if you only want to reason about a single mark or a layer of marks, you don't need to have a view at all.

## View Properties

By default, views don't have any properties.

## Example

Here, we define a single view `v`.

```prolog
property(view,root,v).

property(mark,v,m).
attribute((mark,type),m,tick).
property(encoding,m,e1).
attribute((encoding,channel),e1,x).
attribute((encoding,field),e1,temperature).

property(scale,v,4).
attribute((scale,channel),4,x).
attribute((scale,type),4,linear).
```

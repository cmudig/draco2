# Overview

To express knowledge about visualizations, we first need a language to describe visualizations. Draco describes visualizations and context around them (e.g. properties of the data and task) as _facts_. In this section, we will describe the kinds of facts we chose for Draco.

```{note}
You could design your own description language and use it with Draco or extend the existing language we use here. If you add new information, Draco will not immediately use the new facts until you also add constraints over the facts.
```

The constraint solver Clingo reasons about the facts that describe a visualization. The specific format we use to provide facts to the solver is as a _function_ of the name `property` or `attribute`.

Properties describe what properties exist on an object. If a property has no parents, we use a special object `root`. For example, `property(view,root,v1).` says that there is a view v1 on the root.

Attribute facts specify properties of objects. For example, the number of rows in the dataset in this function form is `attribute(number_rows,root,42).` (read as _the number of rows (on the root object) is 42_).

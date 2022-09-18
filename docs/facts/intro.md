# Overview

To express knowledge about visualizations, we first need a language to describe visualizations. Draco describes
visualizations and context around them (e.g. properties of the data and task) as _facts_. In this section, we will
describe the kinds of facts we chose for Draco.

## Draco has a Generic Specification Format

The constraint solver [Clingo](https://potassco.org/clingo/) reasons about the facts that describe a visualization. The
specific format we use to describe facts to the solver is as a _function_ of the name `entity` or `attribute`.

### Entities

Entities describe objects. The facts `entity` describes what other entities associate with an entity. If an entity has
no parents, we use a special identifier `root`. For example, `entity(view,root,v1).` says that there is a view v1 on the
root.

### Attributes

Attribute facts specify properties of entities. For example, the number of rows in the dataset in this function form is
`attribute(number_rows,root,42).` (read as _the number of rows (on the root entity) is 42_). Attribute names can be
tuples, which allow us to distinguish the same attribute that exists on different entities. For example
`attribute((field,type),f1,number).` specifies the type of a field (here `f1`) while `attribute((mark,type),m1,bar).`
specifies the mark type (here of `m1`).

## Draco's Specification Format for Visualizations

```{note}
You could design your own description language and use it with Draco or extend the existing language we use here. If you add new information, Draco will not immediately use the new facts until you also add constraints over the facts.
```

Draco uses an encoding based on the Grammar of Graphics (GoG) {cite}`wilkinson2012grammar` and Vega-Lite
{cite}`satyanarayan2016vega`. While our specification format is inspired by Vega-Lite, Draco is not limited to the
features Vega-Lite supports.

At the core, a Draco program encodes visualizations in [views](view.md). A view can contain one or more [marks](mark.md)
that [encode](encoding.md) data and corresponding [scales](scale.md). Besides the visualization, a Draco program can
describe the [data schema](schema.md) and the primary [visualization task](task.md). All of these definitions are
extensible and you can add whatever other properties you care about to Draco.

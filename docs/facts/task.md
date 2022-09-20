# Tasks

The task that the user tries to complete when looking at a visualization helps Draco find the most appropriate
visualization.

## Task Properties

`task`
: The task type. Can be one of `value` for reading and comparing values of individual points, and `summary` for comparing aggregate properties. When the task regards specific fields, fields can be marked as relevant
to the task with [`interesting`](schema.md#field-properties).

## Example

```prolog
attribute(task,root,value).
```

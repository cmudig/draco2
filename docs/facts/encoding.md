# Encodings

Encodings define how [data fields](schema.md) map to visual properties (channel) of the [mark](mark.md).

## Encoding Properties

`(encoding,channel)`
: The visual channel. One of `x`, `y`, `color`, `size`, `shape`, or `text`. Same as the [scale channel](scale.md).

`(encoding,field)`
: The field that maps to the visual property of the mark.

`(encoding,aggregate)`
: How the data is aggregated. One of `count`, `mean`, `median`, `min`, `max`, `stdev`, or `sum`.

`(encoding,binning,N)`
: How the data is binned into `N` bins.

`(encoding,stack)`
: One of `zero`, `center`, or `normalize`.

## Example

```prolog
entity(encoding,m,e1).
attribute((encoding,channel),e1,x).
attribute((encoding,field),e1,temperature).
```

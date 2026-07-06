# Data Product Example

This directory contains an example of the Data Product pattern.  It consists of the [Producer](./Producer/docs/sdd.md) component.

This orchestration of components is instantiated in the [ExamplesDeployment](../ExamplesDeployment).

The Producer's `SET_PROC_TYPES` command requests processing (e.g. `PROC_TYPE_ZLIB_DEFLATE`) on its data product containers. The deployment includes the `Svc.DpCompression` subtopology, which losslessly compresses these containers before they are written to disk. An integration test exercising this pipeline is available in [test/int](./test/int).

| Patterns Demonstrated    |
|--------------------------|
| Data Product Pattern    |
| Data Product Compression (DpCompression Subtopology) |

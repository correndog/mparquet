# Meta Parquet

Simple  library to annotate parquet files metadata to add RDF schema information.

Annotating tabular data with RDF can help maintaining the alignment of data sources to a reference vocabulary; alignments that is moved along with the data.

```bash

mparquet -co type-column  -in  ./data/part-result.parquet  -fi dateModified -pr https://data.elsevier.com/lifescience/schema/reaxys/dateModified
mparquet -co type-column  -in  ./data/part-result.parquet  -fi name -pr https://data.elsevier.com/lifescience/schema/reaxys/hasName
mparquet -co type-column  -in  ./data/part-result.parquet  -fi category -pr https://data.elsevier.com/lifescience/schema/reaxys/rder -ub https://data.elsevier.com/lifescience/entity/reaxys/order/
mparquet -co type-column  -in  ./data/part-result.parquet  -fi orderId -pr https://data.elsevier.com/lifescience/schema/reaxys/rder -ub https://data.elsevier.com/lifescience/entity/reaxys/order/
mparquet -co print -in  ./data/part-result.parquet


| name    | value                                                         |
|---------|---------------------------------------------------------------|
| subject | ID                                                            |
| type    | https://data.elsevier.com/lifescience/schema/reaxys/BioAssay  |
| base    | https://data.elsevier.com/lifescience/entity/reaxys/bioassay/ |
| ns      | []                                                            |



| name                             | type          | rdf:property                                                     | base                                                          |
|----------------------------------|---------------|------------------------------------------------------------------|---------------------------------------------------------------|
| ID                               | string        |                                                                  |                                                               |
| name                             | string        | https://data.elsevier.com/lifescience/schema/reaxys/hasName      |                                                               |
| dateCreated                      | timestamp[us] | https://data.elsevier.com/lifescience/schema/reaxys/dateCreated  |                                                               |
| dateModified                     | timestamp[us] | https://data.elsevier.com/lifescience/schema/reaxys/dateModified |                                                               |
| category                         | string        | https://data.elsevier.com/lifescience/schema/reaxys/hasCategory  | https://data.elsevier.com/lifescience/entity/reaxys/category/ |
| assayType                        | string        |                                                                  |                                                               |
| assayDetails                     | string        |                                                                  |                                                               |
| experimentalModel                | string        |                                                                  |                                                               |
| compoundEffect                   | string        |                                                                  |                                                               |
| actionOnTarget                   | string        |                                                                  |                                                               |
| actionOnPhenomenon               | string        |                                                                  |                                                               |
| cellularPhenomenon               | string        |                                                                  |                                                               |
| testsubstanceApplicationLocation | string        |                                                                  |                                                               |
| therapeuticDomain                | string        |                                                                  |                                                               |
| pathology                        | string        |                                                                  |                                                               |
| description                      | string        |                                                                  |                                                               |
| isMainAssayFlag                  | int32         |                                                                  |                                                               |
| isImpFlag                        | string        |                                                                  |                                                               |
| measureFlag                      | int32         |                                                                  |                                                               |
| narrowEffect                     | string        |                                                                  |                                                               |
| orderId                          | string        | https://data.elsevier.com/lifescience/schema/reaxys/hasOrder     | https://data.elsevier.com/lifescience/entity/reaxys/order/    |
| status                           | string        |                                                                  |                                                               |


mparquet -co rdf -of turtle  -in  ./data/part-result.parquet -out ./data/part-result.ttl
mparquet -co rdf -of turtle  -in  ./data/part-result.parquet -out ./data/part-result.ttl
mparquet -co rdf -of json-ld  -in  ./data/part-result.parquet -out ./data/part-result.json
mparquet -co rdf -of hext  -in  ./data/part-result.parquet -out ./data/part-result.hext
mparquet -co print -in  ./data/part-result.parquet

```
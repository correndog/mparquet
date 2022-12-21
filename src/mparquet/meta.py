import pyarrow as pa
import pyarrow.parquet as pq
import sys
from tabulate import tabulate
import json 

__headers__ = ['name' ,'type', 'rdf:property' ,'base']
__rdf_meta__ = {
    'property': b'__rdf__property__' ,
    'subject' : b'__rdf__subject__'  ,
    'base'    : b'__rdf__base__' ,
    'type'    : b'__rdf__subject__type__',
    'namespace' : b'__rdf__namespace__'
}
 
__get_or_none = lambda x,n : None if not x else (json.loads(x[n]) if n in x else None)

def get_schema(filename):
    return pq.read_schema(filename)

def write_table(table, filename):
    pq.write_table( table , filename)

def get_table(filename):
    return pq.read_table(filename)

def getSubject(schema):
    return __get_or_none(schema.metadata , __rdf_meta__['subject'])

def getType(schema):
    return __get_or_none(schema.metadata , __rdf_meta__['type'])

def getColumnBase(schema , columnName):
    return __get_or_none(schema.field(columnName).metadata , __rdf_meta__['base'])

def getSubjectBase(schema ):
    return __get_or_none(schema.metadata , __rdf_meta__['base'])

def getNamespaces(schema ):
    return __get_or_none(schema.metadata , __rdf_meta__['namespace'])


def getColumnProperty(schema , columnName):
    return __get_or_none(schema.field(columnName).metadata , __rdf_meta__['property'])

def print_schema(schema):
    tschema = [
         ('subject' , getSubject(schema)) ,\
         ('type'    , getType(schema)) ,\
         ('base'    , getSubjectBase(schema)),\
         ('ns'      , list(map(lambda ns: ns.split(',') , getNamespaces(schema))) if getNamespaces(schema) else [])
        ]
    print(tabulate(tschema , headers = ['name','value'], tablefmt="github"))
    print("\n\n")
    cschema = [(
                    name , 
                    schema.field(name).type , 
                    __get_or_none(schema.field(name).metadata , __rdf_meta__['property']) ,
                    __get_or_none(schema.field(name).metadata , __rdf_meta__['base']) 
                ) for name in schema.names]
    print(tabulate(cschema , headers = __headers__, tablefmt="github"))

def set_metadata(tbl, col_meta={}, tbl_meta={}):
    """Store table- and column-level metadata as json-encoded byte strings.

    Table-level metadata is stored in the table's schema.
    Column-level metadata is stored in the table columns' fields.

    To update the metadata, first new fields are created for all columns.
    Next a schema is created using the new fields and updated table metadata.
    Finally a new table is created by replacing the old one's schema, but
    without copying any data.

    Args:
        tbl (pyarrow.Table): The table to store metadata in
        col_meta: A json-serializable dictionary with column metadata in the form
            {
                'column_1': {'some': 'data', 'value': 1},
                'column_2': {'more': 'stuff', 'values': [1,2,3]}
            }
        tbl_meta: A json-serializable dictionary with table-level metadata.
    """
    # Create updated column fields with new metadata
    if col_meta or tbl_meta:
        fields = []
        for col in tbl.schema.names:
            if col in col_meta:
                # Get updated column metadata
                metadata = tbl.field(col).metadata or {}
                for k, v in col_meta[col].items():
                    metadata[k] = json.dumps(v).encode('utf-8')
                # Update field with updated metadata
                fields.append(tbl.field(col).with_metadata(metadata))
            else:
                fields.append(tbl.field(col))
        
        # Get updated table metadata
        tbl_metadata = tbl.schema.metadata or {}
        for k, v in tbl_meta.items():
            if type(v)==bytes:
                tbl_metadata[k] = v
            else:
                tbl_metadata[k] = json.dumps(v).encode('utf-8')

        # Create new schema with updated field metadata and updated table metadata
        schema = pa.schema(fields, metadata=tbl_metadata)

        # With updated schema build new table (shouldn't copy data)
        # tbl = pa.Table.from_batches(tbl.to_batches(), schema)
        tbl = tbl.cast(schema )

    return tbl


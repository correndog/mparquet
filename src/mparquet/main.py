from builder import ParquetMetadataBuilder , ModelBuilder
from meta import get_table , print_schema , write_table , set_metadata 
import sys 
import logging 



if __name__ == "__main__":
    logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.DEBUG)
    table = get_table(sys.argv[1])
    mb = ParquetMetadataBuilder()
    mb.addNamespace('reaxys' , 'https://data.elsevier.com/lifescience/schema/reaxys/')\
        .addNamespace('bioassay' , 'https://data.elsevier.com/lifescience/entity/reaxys/bioassay/')\
        .addNamespace('order' , 'https://data.elsevier.com/lifescience/entity/reaxys/order/')\
        .addColumnPropertyMapping('name','https://data.elsevier.com/lifescience/schema/reaxys/hasName')\
        .addColumnPropertyMapping('dateCreated','https://data.elsevier.com/lifescience/schema/reaxys/dateCreated')\
        .addColumnPropertyMapping('dateModified','https://data.elsevier.com/lifescience/schema/reaxys/dateModified')\
        .addColumnPropertyMapping('orderId','https://data.elsevier.com/lifescience/schema/reaxys/hasOrder')\
        .setColumnBase('orderId','https://data.elsevier.com/lifescience/entity/reaxys/order/')\
        .setSubjectColumn('ID')\
        .setSubjectBase('https://data.elsevier.com/lifescience/entity/reaxys/bioassay/')\
        .setSubjectType('https://data.elsevier.com/lifescience/schema/reaxys/BioAssay')    
    mtable = set_metadata(table , 
                            col_meta = mb.columns_metadata,
                            tbl_meta = mb.table_metadata
                )
    print_schema(mtable.schema)
    write_table(mtable , sys.argv[1])
    table = get_table(sys.argv[1])
    mb = ModelBuilder(table)
    gr = mb.getModel()
    gr.serialize(destination = sys.argv[2] , format='turtle')
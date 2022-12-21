from mparquet.meta import getSubject, getType , getSubjectBase , getNamespaces , getColumnProperty , getColumnBase
from rdflib import Graph , URIRef, Literal
from rdflib.namespace import  RDF
from urllib.parse import urlparse
import validators
import logging
import json
class ParquetMetadataBuilder:

    def __init__(self):
        self.table_metadata = {}
        self.columns_metadata = {}

    def addColumnPropertyMapping(self, columnName , propertyURI):
        previous = self.columns_metadata[columnName] if columnName in self.columns_metadata else {}
        previous['__rdf__property__'] = propertyURI  
        self.columns_metadata[columnName] = previous
        return self

    def setSubjectColumn(self , columnName):
        self.table_metadata.update({ '__rdf__subject__' : columnName  })
        return self
    
    def setColumnBase(self , columnName , base):
        previous = self.columns_metadata[columnName] if columnName in self.columns_metadata else {}
        previous['__rdf__base__'] = base  
        self.columns_metadata[columnName] = previous
        return self

    def setSubjectType(self , rdfType):
        self.table_metadata['__rdf__subject__type__'] = rdfType
        return self

    def setSubjectBase(self , base):
        self.table_metadata['__rdf__base__'] = base 
        return self
    
    def addNamespace(self , prefix , path):
        namespaces = self.table_metadata['__rdf__namespace__'] if '__rdf__namespace__' in self.table_metadata else []
        namespaces.append(prefix+","+path)
        self.table_metadata.update({ '__rdf__namespace__' : namespaces  })
        return self
    
    def __str__(self) -> str:
        return json.dumps(self.table_metadata) + '\n' + json.dumps(self.columns_metadata)

class ModelBuilder:

    def __init__(self , table):
        self.table = table
        self.schema = table.schema
        self.subject = getSubject(self.schema)
        self.subjectBase = getSubjectBase(self.schema)
        self.entityType = URIRef(getType(self.schema))
        self.namespaces =  getNamespaces(self.schema)

    def __str__(self) -> str:
        return f"{{ subject : {self.subject}, subjectBase : {self.subjectBase}, entityType : {self.entityType} , namespaces: {self.namespaces} }}"

    def getModel(self) -> Graph:
        g = Graph()
        #Retriieving the namespaces
        for namespace in (self.namespaces if self.namespaces else []):
            prefix , path = namespace.split(',')
            g.bind(prefix,path)
        g.bind("rdf" , RDF)
        faulty = []
        #processing each row as a separate entity
        for row in self.table.to_pylist():
            #setting entity type
            try:
                sURI = self.subjectBase + row[self.subject]
                if validators.url(sURI):
                    s = URIRef(sURI)
                    g.add((s , RDF.type , self.entityType))
                else:
                    faulty += [row]
                    continue
                for columnName in row.keys()-self.subject:
                    if self.schema.field(columnName).metadata and row[columnName]:
                        try:
                            property = URIRef(getColumnProperty(self.schema , columnName))
                            value    = Literal(row[columnName])
                            base     = getColumnBase(self.schema , columnName)
                            if base:
                                oURI = base + row[columnName]
                                if validators.url(oURI):
                                    g.add((s , property , URIRef(oURI)))
                                else:    
                                    faulty += [row]
                            else:
                                g.add((s , property , value)) 
                        except Exception as e:
                            logging.error(self.schema.field(columnName).metadata)    
            except Exception as e:
                logging.error(row)    
        logging.debug("%s errors found."%len(faulty))
        return g
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError

def xml_validator(some_xml_string, xsd_file):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
        print("YEAH!,XML file has validated")
        return [1]
    except Exception as e:
        print("XML not validated .... ")
        print(e)
        return [0, e]

def validate(input):
    xml_file = open(input, 'r')
    xml_string = xml_file.read()
    xml_file.close()
    # return xml_validator(xml_string, 'NHlist-v7_7.xsd')
    return xml_validator(xml_string, 'NHlist-v7_6.xsd')

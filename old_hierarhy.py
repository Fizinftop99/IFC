import sys
import ifcopenshell


# Entity
def traverse(element):
    # element
    yield element
    #print('#' + str(element.id()) + ' = ' + element.is_a() + ' "' + str(element.Name) + '" (' + element.GlobalId + ')')

    # follow Spatial relation
    if element.is_a('IfcSpatialStructureElement'):
        for rel in element.ContainsElements:
            relatedElements = rel.RelatedElements
            for child in relatedElements:
               yield from traverse(child)

    # follow Aggregation Relation
    if element.is_a('IfcObjectDefinition'):
        for rel in element.IsDecomposedBy:
            relatedObjects = rel.RelatedObjects
            for child in relatedObjects:
                yield from traverse(child)


def main():
    # import IFC File
    args = sys.argv
    ifc_file = ifcopenshell.open(args[1])

    items = ifc_file.by_type('IfcProject')
    storeys = []
    for item in items:
        for i in traverse(item):
            if i.is_a("IfcBuildingStorey"):
                storeys.append(i)
    print(storeys)



if __name__ == "__main__":
    main()

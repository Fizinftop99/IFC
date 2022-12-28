import os
from datetime import datetime

import ifcopenshell
from neo4j import GraphDatabase, Session

from graph_utils import add_node, add_edge
from ifc_utils import filter_ifc


def traverse(element: ifcopenshell.entity_instance, parent: ifcopenshell.entity_instance, filter_fn):
    if filter_fn(element):
        yield parent, element
        parent = element

    # follow Spatial relation
    if element.is_a('IfcSpatialStructureElement'):
        for rel in element.ContainsElements:
            relatedElements = rel.RelatedElements
            for child in relatedElements:
                yield from traverse(child, parent, filter_fn)

    # follow Aggregation Relation
    if element.is_a('IfcObjectDefinition'):
        for rel in element.IsDecomposedBy:
            relatedObjects = rel.RelatedObjects
            for child in relatedObjects:
                yield from traverse(child, parent, filter_fn)


# def getChildrenOfType(ifcParentElement, ifcType='IfcSpatialStructureElement'):
#     items = []
#     if not isinstance(ifcType, (list, tuple)):
#         ifcType = [ifcType]
#     _getChildrenOfType(items, ifcParentElement, ifcType, 0)
#     return items
#
#
# def _getChildrenOfType(targetList, element, ifcTypes, level):
#     # follow Spatial relation
#     if element.is_a('IfcSpatialStructureElement'):
#         for rel in element.ContainsElements:
#             relatedElements = rel.RelatedElements
#             for child in relatedElements:
#                 _getChildrenOfType(targetList, child, ifcTypes, level + 1)
#     # follow Aggregation Relation
#     if element.is_a('IfcObjectDefinition'):
#         for rel in element.IsDecomposedBy:
#             relatedObjects = rel.RelatedObjects
#             for child in relatedObjects:
#                 _getChildrenOfType(targetList, child, ifcTypes, level + 1)
#     for typ in ifcTypes:
#         if element.is_a(typ):
#             targetList.append(element)


def graph_from_ifc(session: Session, file_path: str) -> None:
    print(file_path)
    ifc_file = ifcopenshell.open(file_path)
    # k = 0
    for project in ifc_file.by_type("IfcProject"):
        for parent, child in traverse(project, None, filter_ifc):
            # k += 1
            # if k == 10:
            #     break

            session.execute_write(add_node, child)
            if parent is not None:
                # session.execute_write(graph.add_node, parent)
                # print('parent ID:', parent.id(), child.id())
                session.execute_write(add_edge, parent, child)


def main():
    # import IFC File
    # args = sys.argv
    # types = ['IfcSpatialStructureElement', 'IfcObjectDefinition', 'IfcProduct']

    # files = ('model.ifc',
    #          'КЖ_Амундсена_Син_R22_IFC2x3 Coordination View.ifc',
    #          'КЖ_Амундсена_Син_R22_IFC4_Reference_Veiw_Architecture.ifc')

    # filepaths = ('АР_Амундсена_Син_R22.ifc',
    #              'ВК_Амундсена_Син_R22.ifc',
    #              'ГП_Амундсена_Син_R22.ifc',
    #              'КЖ_Амундсена_Син_R22_IFC2x3 Coordination View.ifc',
    #              'КЖ_Амундсена_Син_R22_IFC4 Reference Veiw [Architecture].ifc',
    #              'КЖ_Амундсена_Син_R22_Обновленное_ifc.log',
    #              )
    time = datetime.now()

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "2310"))  # local
    # driver = GraphDatabase.driver("neo4j+s://178ff2cf.databases.neo4j.io:7687", auth=("neo4j", "231099"))
    with driver.session(database='test') as session:
        session.run("Match (n) detach delete n;")
        for _, _, files in os.walk("10_Revit_IFC"):
            for filename in files:
                graph_from_ifc(session, os.path.join("10_Revit_IFC", filename))
                print(datetime.now() - time)
    driver.close()

    print(datetime.now() - time)


if __name__ == "__main__":
    main()

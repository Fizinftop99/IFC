from ifcopenshell import entity_instance


def filter_ifc(element: entity_instance) -> bool:
    return (element.is_a("IfcElement") or element.is_a("IfcSpatialStructureElement")
            or element.is_a("IfcObjectDefinition")) and not element.is_a("IfcGrid")

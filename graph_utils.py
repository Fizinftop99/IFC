from ifcopenshell import entity_instance
from neo4j import Transaction


def get_id(element: entity_instance) -> str:
    # traverce(element)
    return str(element.id())

    # d = {'Категория': 'Уровни',
    #      'Код типа': 'Уровень: Отметка уровня с именем',
    #      'Семейство': 'Уровень: Отметка уровня с именем',
    #      'Семейство и типоразмер': 'Уровень: Отметка уровня с именем',
    #      'Тип': 'Уровень: Отметка уровня с именем',
    #      'id': '399586'}


def add_node(tx: Transaction, node: entity_instance) -> None:
    # d = get_psets(node)
    # try:
    #     print(d['Прочее']['id'])
    #     # props_dict = dict(islice(d['Прочее'].iteritems(), 4))
    #     props_dict: dict = {'id': get_id(node)}
    #     props_str = ' '.join([f'{parse(key)}: {value},' for key, value in props_dict.items()])[:-1]  #
    #
    #     tx.run(f'MERGE (a:Element {{{props_str}}});')
    #     print('norm', get_id(node))
    # except KeyError:
    #     print('empty', get_id(node))
    tx.run('MERGE (e:Element {name: $node_name}) '
           'SET e.id = $node_id, e.type = $node_type;',
           node_id=get_id(node),
           node_name=node.Name,
           node_type=node.is_a(),
           )


def add_edge(tx: Transaction, pred: entity_instance, flw: entity_instance, weight: int = 1) -> None:
    pred_id = get_id(pred)
    flw_id = get_id(flw)
    # print('add_edge', pred_id, flw_id, weight)
    # print('parent:', tx.run('MATCH (pred) WHERE a.id = $id1 RETURN pred', id1=pred_id).data())
    # print('child:', tx.run('MATCH (flw) WHERE a.id = $id1 RETURN flw', id1=flw_id).data())
    # print()
    Q_ADD_REL = '''
    MATCH (a) WHERE a.id = $id1 
    MATCH (b) WHERE b.id = $id2
    MERGE (a)-[r:CONTAINS {weight: $wght}]->(b);
    '''
    tx.run(Q_ADD_REL, id1=pred_id, id2=flw_id, wght=weight)

# def main():
#     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "2310"))
#     with driver.session(database='test') as session:
#         s2 = 'MATCH (n) RETURN n.id AS ID'
#         result = [i['ID'] for i in session.run(s2).data()]
#         print(result)
#     driver.close()
#
#     # s = "RETURN apoc.convert.fromJsonMap('{\"name\": \"Graph Data Science Library\"}') AS output;"
#     # s2 = 'CREATE (a {name:"node", text: "", color: "red", size: "7 m"})'
#
#     # print(res)
#
#
# if __name__ == "__main__":
#     main()

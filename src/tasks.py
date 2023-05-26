from graph import Graph
from data_collection import get_features_as_matrix
from prediction import prediction
import basic_properties as bp


def task_1(graph : Graph, properties : dict) -> tuple:
    if not ('vertices' in properties):
        properties['vertices'] = bp.get_vertices_count(graph)
    if not ('edges' in properties):
        properties['edges'] = bp.get_edges_count(graph) 
    if not ('density' in properties):
        properties['density'] = bp.get_dencity(graph)
    if not ('count_comps' in properties):
        properties['count_comps'] = bp.get_components_count(graph)
    if not ('percentage' in properties):
        properties['percentage'] = bp.get_percentage(graph)

    vertices = properties['vertices']
    edges = properties['edges']
    density = properties['density']
    components = properties['count_comps']
    percentage = properties['percentage']

    heading = ('Vertices', 'Edges', 'Density', 'Components', 'Percentage')
    values = (vertices, edges, density, components, percentage)
    return heading, values

def task_2(graph : Graph, properties : dict) -> tuple:
    if ('radius' in properties) or ('snow' in properties):
        metrics = properties
    else:
        metrics = bp.get_metrics(graph)
        __append_all(metrics, properties) 

    if ('snow' in metrics):
        heading = ('Radius (snow)', 'Diameter (snow)', '90-th (snow)', 
                   'Radius (rand)', 'Diameter (rand)', '90-th (rand)')
        values = (metrics['snow']['radius'], metrics['snow']['diameter'], metrics['snow']['perc90'], 
                  metrics['not_snow']['radius'], metrics['not_snow']['diameter'], metrics['not_snow']['perc90'])
    else:
        heading = ('Radius', 'Diameter', '90-th percentile')
        values = (metrics['radius'], metrics['diameter'], metrics['perc90'])
    
    return heading, values

def task_3(graph : Graph, properties : dict) -> tuple:
    if not ('avg' in properties):
        properties['avg'] = bp.get_avg_coeff(graph)
    
    heading = ('Average clustering coefficient',)
    values = (properties['avg'],)
    return heading, values

def task_4(graph : Graph, properties : dict) -> tuple:
    if not ('assort' in properties):
        properties['assort'] = bp.get_dg_assortativity(graph)

    heading = ('Degree assortativity',)
    values = (properties['assort'],)
    return heading, values

def task_5(dataset : dict, static : bool) -> tuple:
    data = get_features_as_matrix(dataset, static, max_amount=10000, vectors_equalization=True)
    feture_set = 'I' if static else 'II-A'

    if (data is None):
        return None

    heading = ('Precision',)
    values = (prediction(data, dataset['file_name'].split('.')[0], feture_set),)
    return heading, values 

def __append_all(metrics : dict, properties : dict) -> None:
    if ('snow' in metrics):
        properties['snow'] = metrics['snow']
        properties['not_snow'] = metrics['not_snow']
    else:
        properties['radius'] = metrics['radius']
        properties['diameter'] = metrics['diameter']
        properties['perc90'] = metrics['perc90']


import pandas as pd
import base as graphs
import model_training as mdtr

import importlib
importlib.reload(graphs)

def get_stats(network_info):
    
    tmpGraph = graphs.TemporalGraph(network_info['Path'])
    staticGraph = tmpGraph.get_static_graph(0., 1.)
    snowball_sample_approach = graphs.SelectApproach(0, 5)
    random_selected_vertices_approach = graphs.SelectApproach()
    sg_sb = snowball_sample_approach(staticGraph.get_largest_connected_component())
    sg_rsv = random_selected_vertices_approach(staticGraph.get_largest_connected_component())
    # ск - снежный ком
    # свв - случайный выбор вершин
    result = {}
    try:
        result['Сеть'] = network_info['Label']
    except KeyError:
        result['Сеть'] = None

    try:
        result['Категория'] = network_info['Category']
    except KeyError:
        result['Категория'] = None

    try:
        result['Вершины'] = staticGraph.count_vertices()
    except Exception:
        result['Вершины'] = None

    try:
        result['Тип ребер'] = network_info['Edge type']
    except KeyError:
        result['Тип ребер'] = None

    try:
        result['Ребра'] = staticGraph.count_edges()
    except Exception:
        result['Ребра'] = None

    try:
        result['Плот.'] = staticGraph.density()
    except Exception:
        result['Плот.'] = None

    try:
        result['Доля вершин'] = staticGraph.share_of_vertices()
    except Exception:
        result['Доля вершин'] = None

    try:
        result['КСС'] = staticGraph.get_number_of_connected_components()
    except Exception:
        result['КСС'] = None

    try:
        result['Вершины в наиб.КСС'] = staticGraph.get_largest_connected_component().count_vertices()
    except Exception:
        result['Вершины в наиб.КСС'] = None

    try:
        result['Ребра в наиб.КСС'] = staticGraph.get_largest_connected_component().count_edges()
    except Exception:
        result['Ребра в наиб.КСС'] = None

    try:
        result['Радиус(ск)'] = staticGraph.get_radius(sg_sb)
    except Exception:
        result['Радиус(ск)'] = None

    try:
        result['Диаметр(ск)'] = staticGraph.get_diameter(sg_sb)
    except Exception:
        result['Диаметр(ск)'] = None

    try:
        result['90проц.расст.(ск)'] = staticGraph.percentile_distance(sg_sb)
    except Exception:
        result['90проц.расст.(ск)'] = None

    try:
        result['Радиус(свв)'] = staticGraph.get_radius(sg_rsv)
    except Exception:
        result['Радиус(свв)'] = None

    try:
        result['Диаметр(свв)'] = staticGraph.get_diameter(sg_rsv)
    except Exception:
        result['Диаметр(свв)'] = None

    try:
        result['90проц.расст.(свв)'] = staticGraph.percentile_distance(sg_rsv)
    except Exception:
        result['90проц.расст.(свв)'] = None

    try:
        result['Коэф.ассорт.'] = staticGraph.assortative_factor()
    except Exception:
        result['Коэф.ассорт.'] = None

    try:
        result['Ср.кл.коэф.'] = staticGraph.average_cluster_factor()
    except Exception:
        result['Ср.кл.коэф.'] = None

    try:
        result['AUC'] = mdtr.get_performance(tmpGraph, 0.67)
    except Exception:
        result['AUC'] = None

    return result


def graph_features_tables(datasets_info: pd.DataFrame):

    table = pd.DataFrame([get_stats(network_info) for index, network_info in datasets_info.iterrows()]).sort_values('Вершины')
    print(table)

    columns_to_include_to_feature_network_table_1 = [
        'Сеть',
        'Категория',
        'Вершины', 
        'Тип ребер',
        'Ребра',
        'Плот.',
        'Доля вершин',

    ]
    columns_to_include_to_feature_network_table_2 = [
        'Сеть',
        'КСС',
        'Вершины в наиб.КСС',
        'Ребра в наиб.КСС',

    ]
    columns_to_include_to_feature_network_table_3 = [
        'Сеть',
        'Радиус(ск)',
        'Диаметр(ск)',
        '90проц.расст.(ск)',
        'Радиус(свв)',
        'Диаметр(свв)',
        '90проц.расст.(свв)',

    ]
    columns_to_include_to_feature_network_table_4 = [
        'Сеть',
        'Коэф.ассорт.',
        'Ср.кл.коэф.',
    ]

    columns_to_include_to_auc_table = [
        'Сеть',
        'AUC',
    ]
    latex_feature_network_table_1 = table.to_latex(
        formatters={
            'Вершины': lambda x: f'{x:,}', 
            'Ребра': lambda x: f'{x:,}',
            'Плот.': lambda x: f'{x:.6f}',
            'Доля вершин': lambda x: f'{x:.6f}',

        },
        column_format='l@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}r@{\hspace{1em}}r@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}c',
        index=False,
        caption=(
            "Признаки для сетей, рассмотренных в ходе работы "
        ),
        label='Таблица: Признаки сетей',
        escape=False,
        multicolumn=False,
        columns=columns_to_include_to_feature_network_table_1
    )
    latex_feature_network_table_2 = table.to_latex(
        formatters={

            'КСС': lambda x: f'{x:,}',
            'Вершины в наиб.КСС': lambda x: f'{x:,}',
            'Ребра в наиб.КСС': lambda x: f'{x:,}',

        },
        column_format='l@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}r@{\hspace{1em}}r@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}c',
        index=False,
        caption=(
            "Признаки для сетей, рассмотренных в ходе работы "
        ),
        label='Таблица: Признаки сетей',
        escape=False,
        multicolumn=False,
        columns=columns_to_include_to_feature_network_table_2
    )
    latex_feature_network_table_3 = table.to_latex(
        formatters={

            'Радиус(ск)': lambda x: f'{x:.2f}',
            'Диаметр(ск)': lambda x: f'{x:.2f}',
            '90проц.расст.(ск)': lambda x: f'{x:.2f}',
            'Радиус(свв)': lambda x: f'{x:.2f}',
            'Диаметр(свв)': lambda x: f'{x:.2f}',
            '90проц.расст.(свв)': lambda x: f'{x:.2f}',

        },
        column_format='l@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}r@{\hspace{1em}}r@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}c',
        index=False,
        caption=(
            "Признаки для сетей, рассмотренных в ходе работы "
        ),
        label='Таблица: Признаки сетей',
        escape=False,
        multicolumn=False,
        columns=columns_to_include_to_feature_network_table_3
    )
    latex_feature_network_table_4 = table.to_latex(
        formatters={

            'Коэф.ассорт.': lambda x: f'{x:.2f}',
            'Ср.кл.коэф.': lambda x: f'{x:.2f}',
        },
        column_format='l@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}r@{\hspace{1em}}r@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}c',
        index=False,
        caption=(
            "Признаки для сетей, рассмотренных в ходе работы"
        ),
        label='Таблица: Признаки сетей',
        escape=False,
        multicolumn=False,
        columns=columns_to_include_to_feature_network_table_4
    )
    latex_auc_table = table.to_latex(
        formatters={
            'AUC': lambda x: f'{x:.2f}',
        },
        column_format='l@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}r@{\hspace{1em}}r@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{1em}}c@{\hspace{0.5em}}c',
        index=False,
        caption=(
            "Точность пердсказания появления ребер"
        ),
        label='Таблица: AUC',
        escape=False,
        multicolumn=False,
        columns=columns_to_include_to_auc_table
    )
    return (latex_feature_network_table_1,latex_feature_network_table_2,latex_feature_network_table_3,latex_feature_network_table_4,latex_auc_table)
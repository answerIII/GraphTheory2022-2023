import pandas as pd
import python_graphs.visualization as vis

Networks = ['email-Eu-core-temporal-Dept3','opsahl-ucsocial','radoslaw_email',
            'soc-sign-bitcoinalpha','dnc-corecipient','sx-mathoverflow']
networks_files_names = [ f'datasets/{i}/out.{i}' for i in Networks]
number_of_datasets = 6
datasets_info = {'Network': ['email-Eu-core-temporal', 'opsahl-ucsocial','radoslaw_email','soc-sign-bitcoinalpha',
                             'dnc-corecipient','sx-mathoverflow'],
'Label': ['EU','UC','Rado','bitA','Dem ','SX-MO'],
'Category': ['Social',"Information","Social","Social","Social","Social"],
'Edge type': ['Multi','Multi','Multi','Simple','Multi','Multi'],
'Path': networks_files_names}
datasets_info = pd.DataFrame(datasets_info)
datasets_info = datasets_info.iloc[0:5]
print(datasets_info)
latex_feature_network_table_1,latex_feature_network_table_2,latex_feature_network_table_3,latex_feature_network_table_4,latex_auc_table = vis.graph_features_tables(datasets_info)
print(latex_feature_network_table_1)
print(latex_feature_network_table_2)
print(latex_feature_network_table_3)
print(latex_feature_network_table_4)
print(latex_auc_table)

# Temporal Link Prediction
Study project on the subject "Theory of finite graphs".

## Run
 
To run the application, you need to go to the `./src` directory and run the `main.py` script from there. 
Running the script from the `./src` directory is necessary to match the relative paths to the configuration files.

## Adding new datasets

To add a new dataset to the program, you need to upload a `.tsv` file with a graph to the `./data` directory and configure the `./src/config.py` file in accordance with the following paragraph

## Config setup

The `./src/config.py` file describes all the data necessary for the correct processing of datasets. 
Only datasets specified in this file are displayed in the system interface. 
For each dataset that you want to process, you must describe the following parameters:
- `file_name` - The name of the `.tsv` file in the `./data` folder
- `weight_col` - Column number (starting from zero) in which information about the weight of the edge is located in the `.tsv` file
- `timestamp_col` - Column number (starting from zero) in which information about the timestamp of the edge is located in the `.tsv` file
- `number_of_lines_to_skip` - Number of `.tsv` file header lines to skip when parsing
- `filter` - It is measured from 0 to 100 and describes the timestamp by which the time slice of the graph will be performed (set 50 by default)
- `is_multigraph` - When parsing a graph, it does not take into account multiple edges

## Results and tests

- Basic properties on test datasets are in the `./tests/results.txt` file
- The network properties calculated by us (for static graphs) and their comparison with the reference solutions obtained using the `NetworkX` library are located in the folder `./stats`
- Charts for assessing the quality of our model for predicting the appearance of edges in a graph can be found in the folder `./figures`

## Original repository

The original commit history tracking repository can be found at the link: https://github.com/TaisiaSk/temporal-link-prediction.git

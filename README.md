## Important Notes
In your README.md please specify:
- How to run your code
- What language and version your code uses (ie. Python 3.11)
- A list of required packages (i.e. Pandas, NumPy), with version if needed (ie. pytorch==2.1.116)
- If needed, what OS your code should be run on
**Any specifications of this sort not included in your README cannot be assumed to be on the
Directors’ machine(s).**



# README.md for Programming 2024 Project

## Project Overview

This project is developed for the Programming 2024 competition, focusing on identifying optimal offshore drilling locations while considering environmental preservation. Our solution utilizes a combination of obtain and preserve datasets, with informational datasets enhancing our web-based visualization tool. The core algorithm employs a greedy approach with a two-move lookahead strategy to maximize the value and determine the next move efficiently.

## Language and Libraries

- **Language**: Python 3.11
- **Libraries**: numpy, math, csv, json, angular

Ensure you have Python installed on your machine. The code has been developed and tested with Python 3.11. It's recommended to use a similar version to avoid compatibility issues.

## Setup Instructions

1. **Install Required Libraries**:
   
   Before running the project, make sure to install the required Python libraries. Open a terminal or command prompt and run the following command:


`pip install numpy`

Note: `math`, `csv`, and `json` are part of the Python Standard Library and do not require installation.

2. **Clone the Repository**:

Clone the project repository from GitHub to your local machine using the following command:


`git clone https://github.com/Fontaine44/CEC-2024-Yamnuska.git`


3. **Generate the paths**:

To run the algorithms that generate paths, run the following command:

`python CEC-2024-Yamnuska/src/GeneratePaths.py`

This will generate 2 json files corresponding to both path generated for the rigs, and are placed inside the src folder.

4. **Run the web application**:


## Datasets Used

- **Obtain Datasets**: All available datasets for obtainable resources have been utilized to maximize the potential drilling locations.
- **Preserve Dataset**: A single dataset has been chosen for preservation to balance resource extraction with environmental protection. This dataset is the coral dataset.
- **Informational Datasets**: These datasets are used to enhance the visualization on our website, providing users with comprehensive insights into the drilling operations and environmental considerations.

## Algorithm Overview

Our solution is based on a greedy algorithm with a four-move lookahead feature. This approach allows us to evaluate the potential value of drilling locations not just based on their immediate value but also considering the subsequent moves. By maximizing the value at each step, we aim to identify the most optimal drilling locations that respect environmental preservation criteria while ensuring efficient resource extraction.

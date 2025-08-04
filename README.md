# GravitationalCommunityDetection

### Citation:
Please give references for using the algorithms in:

**Gravitational Community Detection:**

Kartlı N., Çetin, P. ve Ayhan S. 2025. New gravitational algorithms for the detection of overlapping and disjoint communities. Kybernetika

## Generating LFR Datasets

It is recommended to produce data with LFR-Benchmark and then use it within the code by `convert_generated_files_into_my_format` function inside the `dataset_generator`.

## Installation of Virtual Environment

If you want to use a virtual environment, you can create and activate it as follows:

**Create a virtual environment:**
```sh
python -m venv venv
```

**Activate the virtual environment:**
```sh
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
```

**Install required packages in requirements.txt file:**
```sh
pip install -r requirements.txt
```

**Run Project:**
```sh
python main.py
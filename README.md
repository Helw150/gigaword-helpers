# My slight modification of the very useful script by Nelson Liu of University of Washignton

# Flattening the Gigaword Datset

The scripts in this repository dump the text of the Gigaword dataset into a single file, for use 
with language modeling (and other!) toolkits.

See my [blog post on flattening the Gigaword corpus](https://blog.nelsonliu.me/2017/09/23/flattening-the-gigaword-corpus/) for 
more information about how the code in this repo works.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation
This project was developed in Python 3.6, but should work with Python 3.x and 2.x.
Please raise an issue if you find that this is not the case.

[Conda](https://conda.io/) will set up a virtual environment with the exact
version of Python used for development along with all the dependencies
needed to run the code in this package.

1.  [Download and install conda](https://conda.io/docs/download.html).

2.  Create a conda environment with Python 3.6.

    ```
    conda create -n flat python=3.6
    ```

3.  Now activate the conda environment.

    ```
    source activate flat
    ```

4.  Install the required dependencies with `pip`.

    ```
    pip install -r requirements.txt
    ```

5.  Install the required SpaCy data pack.
    ```
    python -m spacy download en
    ```
    
## Usage

[`flatten_gigaword.py`](./flatten_gigaword.py) takes in one positional argument and two options:

1.  Postional: The path to the Gigaword directory, with all of the data files unzipped.

2.  `--output-dir`: A directory to write the flattened files to and the final combined output. 
    The default is the current working directory.

3. `--num-parallel`: The number of files to process at once.
   The default is 12 files at once.
   
For example, you can run:

```
./flatten_gigaword.py ./data/gigaword_eng_5/ --output-dir tmp/ --num-parallel 24
```

to extract data (in parallel, processing 24 files at a time) from the Gigaword corpus 
at `./data/gigaword_eng_5/` and write the flattened files + combined output to `tmp/`. 

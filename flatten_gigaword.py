import logging
import os
import re
import spacy

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from multiprocessing import Pool

tokenize = True

def flatten_one_gigaword_file(file_path):
    # Parse the text with BeautifulSoup
    soup = BeautifulSoup(open(file_path), "html.parser")
    
    # Iterate over all <p> items and get the text for each.
    all_paragraphs = []
    for paragraph in soup("p"):
        # Turn inter-paragraph newlines into spaces
        paragraph = paragraph.get_text()
        paragraph = re.sub(r"\n+", "\n", paragraph)
        paragraph = paragraph.replace("\n", " ")

        # Tokenization sometimes needs to be removed
        # (in my case for Multilingual data)
        if tokenize:
            en_nlp = spacy.load("en")
            tokens = en_nlp.tokenizer(paragraph)
            words = [str(token) for token in tokens if not
                     str(token).isspace()]
            if len(words) < 3:
                continue
            else:
                paragraph = " ".join
        all_paragraphs.append(paragraph)
        
    # Return a list of strings, where each string is a
    # space-tokenized paragraph.
    return all_paragraphs

def flatten_and_output(file_path, output_dir):
    all_paragraphs = flatten_one_gigaword_file(file_path)
    output_path = os.path.join(output_dir,
                               os.path.basename(file_path) + ".flat")
    with open(output_path, "w") as output_file:
        for paragraph in all_paragraphs:
            output_file.write("{}\n".format(paragraph))
    return(output_path)



if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser(description=("Flattens gigaword data for "
                                         "use in language modeling."))
    parser.add_argument("gigaword_path",
                        metavar="<gigaword_path>", type=str,
                        help=("Path to Gigaword directory, with "
                              "all .gz files unzipped."))
    parser.add_argument("--output-dir",
                        type=str, default="./",
                        help=("Directory to write flattened Gigaword."))
    parser.add_argument("--final-name",
                        type=str, default="flattened_gigaword.txt",
                        help=("Filename of the final flattened Gigaword."))
    parser.add_argument("--num-parallel", type=int, default="12",
                        help=("The number of Processes to " 
                              "parallelize Gigaword flattening to."))
    parser.add_argument("--cleanup", type=bool,
                        nargs='?', default=False,
                        const=True, help=("Cleanup .flat files after "
                                          "flattening"))
    parser.add_argument("--no-tokenize", type=bool,
                        nargs='?', default=False,
                        const=True, help=("Cleanup .flat files after "
                                          "flattening"))
    
    A = parser.parse_args()
    if A.no_tokenize:
        tokenize = False
    gigaword_files = [(os.path.join(dirpath, filename), A.output_dir)
                      for (dirpath, dirs, files) in os.walk(A.gigaword_path)
                      for filename in (dirs + files)
                      if os.path.isfile(os.path.join(dirpath, filename))]
    pool = Pool(A.num_parallel)
    flat_filenames = pool.starmap(flatten_and_output, gigaword_files)
    with open(A.output_dir+A.final_name, 'w') as outfile:
        for fname in flat_filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    if A.cleanup:
        for fname in flat_filenames:
            os.remove(fname)

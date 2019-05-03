import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
DB_DATABASE = os.environ.get("DB_DATABASE") 

PATH_FEATURE_WORD_VECTORS = os.environ.get("PATH_FEATURE_WORD_VECTORS")
PATH_SRC = os.environ.get("PATH_SRC")
PATH_INPUT_FILES = os.environ.get("PATH_INPUT_FILES")
PATH_OUTPUT_FILES = os.environ.get("PATH_OUTPUT_FILES")
PATH_VECTOR_FILES = os.environ.get("PATH_VECTOR_FILES")
PATH_PLOT_RESULTS = os.environ.get("PATH_PLOT_RESULTS")
PATH_LEXICAL_INDEXED_SRC = os.environ.get("PATH_LEXICAL_INDEXED_SRC")
PATH_METRICAL_INDEXED_SRC = os.environ.get("PATH_METRICAL_INDEXED_SRC")

PATH_METRIC_VALUES = os.environ.get("PATH_METRIC_VALUES")

NUM_LEXICAL_CLUSTERS = int(os.environ.get("NUM_LEXICAL_CLUSTERS"))
NUM_METRICAL_CLUSTERS = int(os.environ.get("NUM_METRICAL_CLUSTERS"))
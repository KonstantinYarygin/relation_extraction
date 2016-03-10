import logging
import logging.config
import os

import yaml

path_to_constants = os.path.dirname(os.path.abspath(__file__))
log_config_name = 'log_conf.yaml'
base_logger_name = 'brightbox_logger'


def setup_logging(
        default_path=os.path.join(path_to_constants, log_config_name),
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            string = f.read()
            config = yaml.load(string)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger(base_logger_name)
pattern_logger = logging.getLogger("pattern_logger")
large_pattern_logger = logging.getLogger("large_pattern_logger")
google_search_nutrient_logger = logging.getLogger("google_search_nutrient_logger")

CLASS_EXCLUSIONS = ['type material', 'genbank acronym', 'acronym']
TEMPLATE_CONTIG = '(_genome[\W\d_]*|_contig[\W\d_]*|_cont[0-9]+)'
TEMPLATE_SEP = '[\W_]+'
RANK_EXCLUSIONS = ['superkingdom', 'kingdom']

FIELD_NAME = 'name'
FIELD_CLASS = 'class'
FIELD_ID = 'id'
FIELD_RANK = 'rank'
FIELD_PARENT_ID = 'parent_id'
CLASS_SCIENTIFIC = 'scientific name'
RANK_SPECIES = 'species'


NCBI_COLS_NAMES = [FIELD_ID, FIELD_NAME, FIELD_CLASS]
NCBI_COLS_NODES = [FIELD_ID, FIELD_PARENT_ID, FIELD_RANK]

NCBI_NUM_NAMES = [0, 2, 6]
NCBI_NUM_NODES = [0, 2, 4]

CHUNK_SIZE = 10000
BACT_KINGDOM_ID_NCBI = 2
BACT_KINGDOM_ID_NCBI = 2157


VERBS = ['degrade', 'utilize', 'produce', 'metabolize','ferment', 'consume', 'hydrolyze', 'require']
MVERBS = ['have ability', 'has ability', 'able', 'can']

PATH_FIELD_TAG = 'tags'
PATH_FIELD_REL = 'edge_rels'
PATH_FIELD_WORD = 'words'
PATH_FIELD_IND = 'pos_path'

PATH_NUTR_NAME = 'NUTRIENT'
PATH_BACT_NAME = 'BACTERIUM'

VERB_LIST = ['consume', 'acquire', 'absorb', 'ingest', 'retain', 'adhere', 'adopt', 'assimilate', 'obtain',
             'incorporate', 'eat', 'degrade', 'utilize', 'utilise', 'metabolize', 'metabolise', 'ferment',
             'hydrolyze', 'cleave', 'catabolize', 'digest', 'bind', 'hydrolyse', 'lyse', 'convert', 'oxidize',
             'destroy', 'eliminate', 'dephosphorylate', 'exploit', 'transform', 'eradicate', 'dissociate',
             'deactivate', 'neutralize', 'dimerize', 'inactivate', 'phosphorylate', 'heterodimerizes',
             'produce', 'synthesize', 'synthesise', 'biosynthesize', 'biosynthesise', 'assemble',
             'create', 'make', 'secrete', 'excrete', 'liberate', 'attach', 'resist', 'transmit', 'disseminate',
             'solubilize', 'sustain', 'adapt', 'neutralize']
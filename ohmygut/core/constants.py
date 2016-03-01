
CLASS_EXCLUSIONS = ['type material', 'genbank acronym', 'acronym']
TEMPLATE_CONTIG = '(_genome[\W\d_]*|_contig[\W\d_]*|_cont[0-9]+)'
TEMPLATE_SEP = '[\W_]+'
RANK_EXCLUSIONS = ['superkingdom']

FIELD_NAME = 'name'
FIELD_UNIQUE_NAME = 'unique_name'
FIELD_CLASS = 'class'
FIELD_ID = 'id'
FIELD_RANK = 'rank'
FIELD_PARENT_ID = 'parent_id'
CLASS_SCIENTIFIC = 'scientific name'
RANK_SPECIES = 'species'


NCBI_COLS_NAMES = [FIELD_ID, FIELD_UNIQUE_NAME, FIELD_CLASS]
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

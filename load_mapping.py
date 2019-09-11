import logging

def _load_mapping(f_name):
    '''
    Prepares a map of token and its occurrences from
    a file containing the word and its occurrences
    '''

    f = open(f_name)
    tok_to_occur_map = {}
    logging.info("started loading mappings")
    for line in f:
        token, occur = line.strip().split("\t")
        tok_to_occur_map[token] = int(occur)
    logging.info("loading completed")

    return tok_to_occur_map

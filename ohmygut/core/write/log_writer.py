from ohmygut.core.constants import pattern_logger, large_pattern_logger
from ohmygut.core.write.base_writer import BaseWriter


class LogWriter(BaseWriter):
    def write(self, sentence):
        if len(sentence.shortest_paths) > 0:
            log_paths(sentence)


def log_paths(sentence):
    # todo: почему не объединять вывод? например:
    # pattern_logger.info('%s \n %s \n %s \n' % (sentence.text, sentence.bacteria, sentence.nutrients))

    pattern_logger.info(sentence.text)
    pattern_logger.info(sentence.bacteria)
    pattern_logger.info(sentence.nutrients)
    pattern_logger.info('')

    for pair_type, pathes in sentence.shortest_paths.items():
        for path in pathes:
            pattern_logger.info(pair_type)
            pattern_logger.info(path.words)
            # pattern_logger.info(path.type)
            pattern_logger.info('')
    pattern_logger.info('=' * 100)
    pattern_logger.info('')

    large_pattern_logger.info(sentence.text)
    large_pattern_logger.info(sentence.bacteria)
    large_pattern_logger.info(sentence.nutrients)
    large_pattern_logger.info('')
    large_pattern_logger.info(sentence.parser_output.words)
    large_pattern_logger.info(sentence.parser_output.tags)
    large_pattern_logger.info(sentence.parser_output.nx_graph)
    large_pattern_logger.info([(i, j, sentence.parser_output.nx_graph[i][j]['rel']) for i, j in
                               sentence.parser_output.nx_graph.edges()])
    large_pattern_logger.info('')

    for pair_type, pathes in sentence.shortest_paths.items():
        for path in pathes:
            large_pattern_logger.info(pair_type)
            large_pattern_logger.info(path.words)
            large_pattern_logger.info(path.edge_rels)
            large_pattern_logger.info(path.tags)
            large_pattern_logger.info(path.nodes_indexes)
            # large_pattern_logger.info(path.type)
            large_pattern_logger.info('')

    large_pattern_logger.info('=' * 100)
    large_pattern_logger.info('')

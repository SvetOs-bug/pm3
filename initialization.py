from uniparser_morph import Analyzer
import pymorphy3


def initialize_uniparser():
    analyzer = Analyzer()
    analyzer.lexFile = "lexemes.txt"
    analyzer.paradigmFile = "paradigms.txt"
    analyzer.load_grammar()

    return analyzer


def initialize_pymorphy():
    return pymorphy3.MorphAnalyzer()
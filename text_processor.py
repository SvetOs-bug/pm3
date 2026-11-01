import re
from grammar_dictionary import full_grammemes


class TextProcessor:

    def __init__(self, uniparser, pymorphy):
        self.uniparser = uniparser
        self.pymorphy = pymorphy

    def replace_word(self, text):
        parts = re.split(r'([,\s|]+)', text)

        return ''.join(
            full_grammemes.get(part, part)
            for part in parts
        )

    def analyze_sentence(self, sentence):

        tokens = re.findall(
            r"\w+(?:[-’']\w+)*|[^\w\s]",
            sentence,
            re.UNICODE
        )

        uniparser_results = self.uniparser.analyze(tokens)

        results = []
        uniparser_count = 0
        pymorphy_count = 0

        for word in tokens:

            if not re.search(r"\w", word, re.UNICODE):
                results.append({
                    "word": word,
                    "lemma": "—",
                    "grammar": "Знак пунктуации",
                    "analyzer": "—"
                })
                continue

            if word.casefold() in uniparser_results:

                data = uniparser_results[word.casefold()]

                lemma = data["lemma"]
                grammar = data["grammar"]
                analyzer_name = "UniParser"

                uniparser_count += 1

            else:

                data = self.pymorphy.analyze(word)

                lemma = data["lemma"]
                grammar = data["grammar"]
                analyzer_name = "pymorphy3"

                pymorphy_count += 1

            grammar = self.replace_word(grammar)

            results.append({
                "word": word,
                "lemma": lemma,
                "grammar": grammar,
                "analyzer": analyzer_name
            })

        return {
            "results": results,
            "total": len(tokens),
            "uniparser_count": uniparser_count,
            "pymorphy_count": pymorphy_count
        }
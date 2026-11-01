class UniParserAnalyzer:

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self, tokens):
        result = self.analyzer.analyze_words(
            [tokens],
            format="conll"
        )

        lines = (
            result.splitlines()
            if isinstance(result, str)
            else str(result).splitlines()
        )

        results = {}

        for line in lines:
            parts = line.split("\t")

            if len(parts) >= 7:
                word = parts[1]

                if parts[2] != "_" and parts[4] != "_":
                    results[word.casefold()] = {
                        "lemma": parts[2],
                        "grammar": parts[4]
                    }

        return results


class PymorphyAnalyzer:

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self, word):
        parsed = self.analyzer.parse(word)[0]

        return {
            "lemma": parsed.normal_form,
            "grammar": str(parsed.tag)
        }
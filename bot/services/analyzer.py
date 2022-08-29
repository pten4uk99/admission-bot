from pullenti import Sdk
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Processor import Processor
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.keyword.KeywordReferent import KeywordReferent
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer


class Analyzer:
    def __init__(self):
        Sdk.Sdk.initialize_all()
        self.processor = self._create_processor()
        self.result: AnalysisResult = None

    def _create_processor(self) -> Processor:
        return ProcessorService().create_specific_processor(KeywordAnalyzer.ANALYZER_NAME)

    def analyze(self, text):
        sofa = SourceOfAnalysis(text)
        self.result = self.processor.process(sofa)

    def data(self):
        result = []

        for entity in self.result.entities:
            entity: KeywordReferent
            print(entity, entity.__class__)
            result.append(entity.to_string(short_variant=True, lang=MorphLang()))

        return '\n'.join(result)


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.analyze('Контакты приемной комиссии')
    analyzer.data()

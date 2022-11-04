from pullenti import Sdk
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.Processor import Processor
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.keyword.KeywordAnalyzer import KeywordAnalyzer
from pullenti.ner.keyword.KeywordReferent import KeywordReferent

from db.models import Keyword, Comparison
from services.exceptions import WrongReferent
from services.support_keywords import SUPPORT_KEYWORDS


class Result:
    def __init__(self, data: AnalysisResult):
        self._data = data

    @property
    def _data(self) -> list[KeywordReferent]:
        return self.__data

    @_data.setter
    def _data(self, value: AnalysisResult):
        assert isinstance(value, AnalysisResult), (
            f'{self.__class__}: "result" атрибут должен быть типо {AnalysisResult}'
        )

        self.__data = self._filter_entities(value.entities)

    def _filter_entities(self, entities: list[KeywordReferent]) -> list[KeywordReferent]:
        """ Возвращает элементы списка, у которых только одно слово """

        filtered = []
        for entity in entities:
            try:
                value = self._get_entity_value(entity)
            except WrongReferent:
                continue

            if ' ' not in value:
                filtered.append(entity)

        return filtered

    @staticmethod
    def _get_entity_value(referent: KeywordReferent) -> str:
        """ Нормализированное значение - приоритетное """

        if not isinstance(referent, KeywordReferent):
            raise WrongReferent(f'"referent" должен быть типа {KeywordReferent}')

        if getattr(referent, 'normal_value', None) is not None:
            return referent.normal_value
        return referent.value

    def to_list(self) -> list[str]:
        """ Возвращает данные в виде списка """

        result = []

        for entity in self._data:
            value = self._get_entity_value(entity)
            result.append(value)

        return result


class Analyzer:
    """
    Анализирует переданный текст с помощью pullenti.

    Использование:
    1. Инициализировать объект
    self.analyze() - анализирует переданный текст
    self.result - сохраняет результат анализа
    self.clear() - отчищает результат анализа
    """

    __result: Result = None

    def __init__(self):
        Sdk.Sdk.initialize_all()
        self.processor = self._create_processor()

    def clear(self):
        """ Отчищает результат анализа """

        self.__result = None

    @property
    def result(self) -> Result:
        return self.__result

    @result.setter
    def result(self, value: AnalysisResult):
        assert isinstance(value, AnalysisResult), (
            f'{self.__class__}: "result" атрибут должен быть типо {AnalysisResult}'
        )
        self.__result = Result(value)

    def _create_processor(self) -> Processor:
        return ProcessorService().create_specific_processor(KeywordAnalyzer.ANALYZER_NAME)

    def analyze(self, text) -> None:
        sofa = SourceOfAnalysis(text)
        self.result = self.processor.process(sofa)


class AnalysisManager:
    analyzer = Analyzer()

    def __init__(self, text: str):
        self.analyzer.clear()
        self.text = text

    def _get_support_keywords(self):
        """ Проверяет дополнительные ключевые слова, которые пулленти не может анализировать """

        result = []
        for keyword in SUPPORT_KEYWORDS:
            if keyword.upper() in self.text.upper():
                result.append(keyword.upper())
        return result

    def _get_analyzed_keywords(self) -> set[str]:
        """ Возвращает ключевые слова, которые получилось выявить из переданного текста """

        self.analyzer.analyze(self.text)
        analyzed = self.analyzer.result.to_list()
        support = self._get_support_keywords()

        return set(analyzed + support)

    def _get_db_keywords(self) -> list[Keyword]:
        """
        Возвращает совпадения по ключевым словам,
        выявленным из текста с ключевыми словами в базе данных
        """

        analyzed_keywords = self._get_analyzed_keywords()
        Keyword.query_.get(source__in=analyzed_keywords)
        return Keyword.query_.perform_fetch(many=True)

    def _get_comparions_list(self, keywords: list[Keyword]):
        comparison_id_list = []
        for keyword in keywords:
            if keyword.comparison not in comparison_id_list:
                comparison_id_list.append(keyword.comparison)

        Comparison.query_.get(pk__in=comparison_id_list)
        return Comparison.query_.perform_fetch(many=True)

    def answer(self) -> list[str]:
        keywords = self._get_db_keywords()
        comparisons: list[Comparison] = self._get_comparions_list(keywords)

        answers = []
        for comparison in comparisons:
            answers.append(comparison.answer)
        return answers


if __name__ == '__main__':
    manager = AnalysisManager('Руководитель творческой мастерской')
    print(manager._get_analyzed_keywords())

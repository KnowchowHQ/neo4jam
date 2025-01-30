# TODO Use DeepEval library for evaluation metrics (https://www.confident-ai.com/blog/how-to-evaluate-llm-applications)

# This module is responsible to run the following LLM evaluation metrics.
import evaluate

from abc import ABC, abstractmethod

# Abstract Product (Evaluation Metric)
class EvaluationMetric(ABC):
    @abstractmethod
    def calculate(self, predictions, references):
        """Calculate the evaluation metric."""
        pass


# Concrete Products (Specific Metrics)
class BLEUMetric(EvaluationMetric):
    def calculate(self, predictions, references):
        # Implement BLEU calculation logic
        evaluation_metric = evaluate.load("bleu")
        scores = evaluation_metric.compute(predictions=predictions, references=references)
        return scores


class ROUGEMetric(EvaluationMetric):
    def calculate(self, predictions, references):
        # Implement ROUGE calculation logic
        evaluation_metric = evaluate.load("rouge")
        scores = evaluation_metric.compute(predictions=predictions, references=references)
        return scores


# Abstract Factory
class MetricFactory(ABC):
    @abstractmethod
    def create_metric(self) -> EvaluationMetric:
        """Create a specific evaluation metric."""
        pass


# Concrete Factories
class BLEUMetricFactory(MetricFactory):
    def create_metric(self) -> EvaluationMetric:
        return BLEUMetric()


class ROUGEMetricFactory(MetricFactory):
    def create_metric(self) -> EvaluationMetric:
        return ROUGEMetric()


# Client Code
def evaluate_model(factory: MetricFactory, predictions, references):
    metric = factory.create_metric()
    return metric.calculate(predictions, references)
# TODO Use DeepEval library for evaluation metrics (https://www.confident-ai.com/blog/how-to-evaluate-llm-applications)

# This module is responsible to run the following LLM evaluation metrics.

import evaluate
from abc import ABC, abstractmethod
from loguru import logger


# Abstract Product (Evaluation Metric)
class EvaluationMetric(ABC):
    @abstractmethod
    def calculate(self, predictions, references):
        """Calculate the evaluation metric."""
        pass


# Concrete Products (Specific Metrics)
class BLEUMetric(EvaluationMetric):
    def __init__(self): 
        # Implement BLEU calculation logic
        logger.info("BLEU metric loaded.")
        self.evaluation_metric = evaluate.load("bleu")
    
    def calculate(self, predictions, references):
        scores = self.evaluation_metric.compute(predictions=predictions, references=references)
        return scores


class ROUGEMetric(EvaluationMetric):
    def __init__(self):
        logger.info("ROUGE metric loaded.")
        self.evaluation_metric = evaluate.load("rouge")

    def calculate(self, predictions, references):
        # Implement ROUGE calculation logic
        scores = self.evaluation_metric.compute(predictions=predictions, references=references)
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
def evaluate_model(metric: EvaluationMetric, predictions, references):
    metric = metric.create_metric()
    return metric.calculate(predictions, references)

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class PIIDetector:
    def __init__(self):
        try:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            logger.info("PII Detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PII Detector: {e}")
            raise

    async def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect PII in text
        """
        try:
            results = self.analyzer.analyze(text=text, language='en')
            entities = [
                {
                    "type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score
                }
                for result in results
            ]
            return {
                "has_pii": len(entities) > 0,
                "entities": entities,
                "anonymized_text": None
            }
        except Exception as e:
            logger.error(f"Error detecting PII: {e}")
            raise

    async def anonymize(self, text: str) -> Dict[str, Any]:
        """
        Anonymize PII in text
        """
        try:
            analyzer_results = self.analyzer.analyze(text=text, language='en')
            anonymized_result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results
            )
            
            entities = [
                {
                    "type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score
                }
                for result in analyzer_results
            ]
            
            return {
                "has_pii": len(entities) > 0,
                "entities": entities,
                "anonymized_text": anonymized_result.text
            }
        except Exception as e:
            logger.error(f"Error anonymizing PII: {e}")
            raise

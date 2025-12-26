"""
Accuracy Calculator Module
Combines fuzzy string matching (RapidFuzz) with semantic embeddings
for accurate, fast, and reliable accuracy calculation
"""

import json
import re
from typing import Dict, List, Any, Optional
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import Settings, get_settings


class AccuracyCalculator:
    """Calculates accuracy using fuzzy matching + semantic embeddings"""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize accuracy calculator
        
        Args:
            settings: Settings instance (if None, uses get_settings())
        """
        self.settings = settings or get_settings()
        self.embedding_model = None
        self._initialize_embedding_model()
    
    def _initialize_embedding_model(self):
        """Initialize the embedding model (lazy loading)"""
        try:
            self.embedding_model = SentenceTransformer(self.settings.embedding_model_name)
        except Exception as e:
            print(f"Warning: Could not load embedding model: {e}")
            print("Falling back to fuzzy matching only")
            self.embedding_model = None
    
    def _extract_string_from_value(self, value: Any) -> str:
        """
        Extract string value from various types (handles arrays/lists and nested objects)
        
        Args:
            value: Value that may be a string, list, dict, or other type
            
        Returns:
            String representation of the value
        """
        if isinstance(value, list):
            if len(value) == 0:
                return ""
            elif len(value) == 1:
                return str(value[0]).strip()
            else:
                return ", ".join(str(item).strip() for item in value if item)
        elif isinstance(value, dict):
            nested_values = []
            for key, val in value.items():
                if isinstance(val, list):
                    nested_values.extend([str(item).strip() for item in val if item])
                else:
                    nested_values.append(str(val).strip() if val else "")
            return ", ".join(v for v in nested_values if v)
        else:
            return str(value).strip() if value else ""
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison - removes formatting differences
        
        Args:
            text: Input text to normalize
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        text = str(text).strip()
        
        # Remove number prefixes like "1. ", "2. ", etc.
        text = re.sub(r'^\d+\.\s*', '', text)
        
        # Remove bullet points
        text = re.sub(r'^[•\-*]\s*', '', text)
        
        # Normalize common abbreviations
        text = re.sub(r'\bco-op\b', 'co-operative', text, flags=re.IGNORECASE)
        text = re.sub(r'\bco\.\s*op\.', 'co-operative', text, flags=re.IGNORECASE)
        text = re.sub(r'\bltd\.', 'limited', text, flags=re.IGNORECASE)
        text = re.sub(r'\binc\.', 'incorporated', text, flags=re.IGNORECASE)
        
        # Remove trailing punctuation
        text = re.sub(r'[.,;:]+$', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.lower().strip()
    
    def _calculate_fuzzy_similarity(self, actual: str, predicted: str) -> Dict[str, float]:
        """
        Calculate fuzzy similarity using multiple algorithms
        
        Args:
            actual: Actual value
            predicted: Predicted value
            
        Returns:
            Dictionary with different similarity scores
        """
        actual_norm = self._normalize_text(actual)
        predicted_norm = self._normalize_text(predicted)
        
        scores = {
            'ratio': fuzz.ratio(actual_norm, predicted_norm) / 100.0,
            'partial_ratio': fuzz.partial_ratio(actual_norm, predicted_norm) / 100.0,
            'token_sort_ratio': fuzz.token_sort_ratio(actual_norm, predicted_norm) / 100.0,
            'token_set_ratio': fuzz.token_set_ratio(actual_norm, predicted_norm) / 100.0,
        }
        
        return scores
    
    def _calculate_semantic_similarity(self, actual: str, predicted: str) -> float:
        """
        Calculate semantic similarity using embeddings
        
        Args:
            actual: Actual value
            predicted: Predicted value
            
        Returns:
            Similarity score between 0 and 1
        """
        if not self.embedding_model:
            return 0.0
        
        try:
            embeddings = self.embedding_model.encode([actual, predicted], convert_to_numpy=True)
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return max(0.0, min(1.0, float(similarity)))
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def _calculate_field_accuracy(self, actual: Any, predicted: str, field_name: str) -> Dict[str, Any]:
        """
        Calculate accuracy for a single field using hybrid approach
        
        Args:
            actual: Actual value from JSON
            predicted: Predicted value from LLM output
            field_name: Name of the field (for field-specific logic)
            
        Returns:
            Dictionary with accuracy score and details
        """
        actual_str = self._extract_string_from_value(actual)
        predicted_str = str(predicted).strip() if predicted else ""
        
        if not actual_str and not predicted_str:
            return {
                "accuracy": 1.0,
                "method": "exact_match",
                "details": "Both empty"
            }
        
        if not actual_str or not predicted_str:
            return {
                "accuracy": 0.0,
                "method": "empty_mismatch",
                "details": "One empty, other not"
            }
        
        # Exact match (case-insensitive)
        if actual_str.lower().strip() == predicted_str.lower().strip():
            return {
                "accuracy": 1.0,
                "method": "exact_match",
                "details": "Exact match"
            }
        
        # Normalized exact match
        actual_norm = self._normalize_text(actual_str)
        predicted_norm = self._normalize_text(predicted_str)
        
        if actual_norm == predicted_norm:
            return {
                "accuracy": 1.0,
                "method": "normalized_exact",
                "details": "Normalized exact match"
            }
        
        # Calculate fuzzy similarity scores
        fuzzy_scores = self._calculate_fuzzy_similarity(actual_str, predicted_str)
        
        # Weighted fuzzy score
        fuzzy_score = (
            fuzzy_scores['ratio'] * 0.2 +
            fuzzy_scores['partial_ratio'] * 0.2 +
            fuzzy_scores['token_sort_ratio'] * 0.3 +
            fuzzy_scores['token_set_ratio'] * 0.3
        )
        
        # Decision logic: when to use semantic similarity
        use_semantic = False
        
        # For fields that need semantic understanding, use embeddings if fuzzy score is in ambiguous range
        if field_name.lower() not in ["flat no", "flat_no", "document_number", "document number"]:
            if 0.80 <= fuzzy_score < 0.95:
                use_semantic = True
        
        if use_semantic and self.embedding_model:
            semantic_score = self._calculate_semantic_similarity(actual_str, predicted_str)
            final_score = (fuzzy_score * 0.6 + semantic_score * 0.4)
            
            return {
                "accuracy": final_score,
                "method": "hybrid",
                "fuzzy_score": fuzzy_score,
                "semantic_score": semantic_score,
                "details": f"Hybrid: fuzzy={fuzzy_score:.2%}, semantic={semantic_score:.2%}"
            }
        else:
            return {
                "accuracy": fuzzy_score,
                "method": "fuzzy",
                "fuzzy_scores": fuzzy_scores,
                "details": f"Fuzzy matching: {fuzzy_score:.2%}"
            }
    
    def _extract_predicted_values(self, llm_output: str, actual_doc: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract predicted values from LLM output (handles both JSON and text formats)
        
        Args:
            llm_output: LLM output (may be JSON or text)
            actual_doc: Actual document data for field name matching
            
        Returns:
            Dictionary mapping actual field names to predicted values
        """
        predicted_values = {}
        llm_json = None
        
        # Strategy 1: Try to find JSON in code blocks (```json ... ```)
        try:
            code_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            matches = re.findall(code_block_pattern, llm_output, re.DOTALL)
            if matches:
                json_text = matches[-1].strip()
                llm_json = json.loads(json_text)
        except (json.JSONDecodeError, AttributeError, IndexError):
            pass
        
        # Strategy 2: Try to find any JSON object in the text
        if llm_json is None:
            try:
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                matches = re.findall(json_pattern, llm_output, re.DOTALL)
                if matches:
                    for match in matches:
                        try:
                            llm_json = json.loads(match)
                            break
                        except json.JSONDecodeError:
                            continue
            except (json.JSONDecodeError, AttributeError):
                pass
        
        # Strategy 3: Try to parse entire output as JSON
        if llm_json is None:
            try:
                json_text = llm_output.strip()
                if json_text.startswith('```'):
                    lines = json_text.split('\n')
                    if lines[0].strip().startswith('```'):
                        json_text = '\n'.join(lines[1:])
                if json_text.endswith('```'):
                    json_text = json_text[:-3].strip()
                
                llm_json = json.loads(json_text)
            except (json.JSONDecodeError, AttributeError):
                pass
        
        # If we found JSON, map fields to actual field names
        if llm_json:
            for actual_field_name in actual_doc.keys():
                if actual_field_name == "Document id":
                    continue
                
                actual_field_lower = actual_field_name.lower().strip()
                actual_field_base = actual_field_lower.split('/')[0].strip()
                actual_field_normalized = re.sub(r'[_\s-]+', '', actual_field_lower)
                actual_field_base_normalized = re.sub(r'[_\s-]+', '', actual_field_base)
                
                found_value = None
                
                for llm_key, llm_value in llm_json.items():
                    llm_key_lower = str(llm_key).lower().strip()
                    llm_key_base = llm_key_lower.split('/')[0].strip()
                    llm_key_normalized = re.sub(r'[_\s-]+', '', llm_key_lower)
                    llm_key_base_normalized = re.sub(r'[_\s-]+', '', llm_key_base)
                    
                    if (actual_field_lower == llm_key_lower or 
                        actual_field_base == llm_key_base or
                        actual_field_base == llm_key_lower or
                        actual_field_lower == llm_key_base or
                        actual_field_normalized == llm_key_normalized or
                        actual_field_base_normalized == llm_key_base_normalized or
                        actual_field_lower.replace(' ', '') == llm_key_lower.replace(' ', '') or
                        actual_field_base.replace(' ', '') == llm_key_base.replace(' ', '') or
                        actual_field_lower.replace('_', ' ') == llm_key_lower.replace('_', ' ')):
                        
                        if isinstance(llm_value, (dict, list)):
                            found_value = self._extract_string_from_value(llm_value)
                        else:
                            found_value = str(llm_value).strip()
                        break
                
                if found_value:
                    predicted_values[actual_field_name] = found_value
        
        # Strategy 4: If JSON extraction failed, try regex patterns
        if not predicted_values:
            for actual_field_name in actual_doc.keys():
                if actual_field_name == "Document id":
                    continue
                
                field_patterns = [
                    rf'"{re.escape(actual_field_name)}"\s*:\s*"([^"]+)"',
                    rf'"{re.escape(actual_field_name.split("/")[0])}"\s*:\s*"([^"]+)"',
                    rf'{re.escape(actual_field_name)}[:\s]+"([^"]+)"',
                    rf'{re.escape(actual_field_name.split("/")[0])}[:\s]+"([^"]+)"',
                ]
                
                field_lower = actual_field_name.lower()
                field_patterns.extend([
                    rf'"{re.escape(field_lower)}"\s*:\s*"([^"]+)"',
                    rf'{re.escape(field_lower)}[:\s]+"([^"]+)"',
                ])
                
                for pattern in field_patterns:
                    match = re.search(pattern, llm_output, re.IGNORECASE | re.DOTALL)
                    if match:
                        predicted_values[actual_field_name] = match.group(1).strip()
                        break
        
        return predicted_values
    
    def calculate_accuracy(
        self, 
        llm_output: str, 
        actual_data: Dict[str, Any],
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate accuracy for a single document
        
        Args:
            llm_output: Output from LLM (can be verbose text or JSON)
            actual_data: Actual document data (dict with field names as keys)
            document_id: Optional document identifier
            
        Returns:
            Dictionary with accuracy metrics
        """
        # Extract predicted values from LLM output
        predicted_values = self._extract_predicted_values(llm_output, actual_data)
        
        # Calculate accuracy for each field
        fields_accuracy = {}
        total_accuracy = 0.0
        field_count = 0
        
        for field_name in actual_data.keys():
            if field_name == "Document id":
                continue
            
            actual_value = actual_data[field_name]
            
            # Handle nested objects
            if isinstance(actual_value, dict):
                predicted_value = predicted_values.get(field_name, "")
                
                if not predicted_value:
                    field_name_lower = field_name.lower().strip()
                    field_name_base = field_name_lower.split('/')[0].strip()
                    for pred_key, pred_val in predicted_values.items():
                        pred_key_lower = str(pred_key).lower().strip()
                        pred_key_base = pred_key_lower.split('/')[0].strip()
                        field_normalized = re.sub(r'[_\s/-]+', '', field_name_lower)
                        pred_normalized = re.sub(r'[_\s/-]+', '', pred_key_lower)
                        field_base_normalized = re.sub(r'[_\s/-]+', '', field_name_base)
                        pred_base_normalized = re.sub(r'[_\s/-]+', '', pred_key_base)
                        
                        if (pred_key_lower == field_name_lower or 
                            pred_key_base == field_name_base or
                            pred_key_base == field_name_lower or
                            pred_key_lower == field_name_base or
                            field_normalized == pred_normalized or
                            field_base_normalized == pred_base_normalized or
                            field_name_lower in pred_key_lower or 
                            pred_key_lower in field_name_lower):
                            
                            if isinstance(pred_val, (dict, list)):
                                predicted_value = self._extract_string_from_value(pred_val)
                            else:
                                predicted_value = str(pred_val).strip()
                            break
                
                field_result = self._calculate_field_accuracy(actual_value, predicted_value, field_name)
                actual_str_display = self._extract_string_from_value(actual_value)
            else:
                predicted_value = predicted_values.get(field_name, "")
                
                if not predicted_value:
                    field_name_lower = field_name.lower().strip()
                    field_name_base = field_name_lower.split('/')[0].strip()
                    for pred_key, pred_val in predicted_values.items():
                        pred_key_lower = str(pred_key).lower().strip()
                        pred_key_base = pred_key_lower.split('/')[0].strip()
                        field_normalized = re.sub(r'[_\s/-]+', '', field_name_lower)
                        pred_normalized = re.sub(r'[_\s/-]+', '', pred_key_lower)
                        field_base_normalized = re.sub(r'[_\s/-]+', '', field_name_base)
                        pred_base_normalized = re.sub(r'[_\s/-]+', '', pred_key_base)
                        
                        if (field_name_lower == pred_key_lower or 
                            field_name_base == pred_key_base or
                            field_name_base == pred_key_lower or
                            field_name_lower == pred_key_base or
                            field_normalized == pred_normalized or
                            field_base_normalized == pred_base_normalized or
                            field_name_lower.replace(' ', '') == pred_key_lower.replace(' ', '')):
                            predicted_value = pred_val
                            break
                
                field_result = self._calculate_field_accuracy(actual_value, predicted_value, field_name)
                actual_str_display = self._extract_string_from_value(actual_value)
            
            fields_accuracy[field_name] = {
                "accuracy": field_result["accuracy"],
                "actual": actual_str_display,
                "predicted": predicted_value,
                "method": field_result.get("method", "unknown"),
                "details": field_result.get("details", "")
            }
            
            total_accuracy += field_result["accuracy"]
            field_count += 1
        
        # Calculate overall accuracy
        overall_accuracy = total_accuracy / field_count if field_count > 0 else 0.0
        
        return {
            "document_id": document_id,
            "accuracy": overall_accuracy,
            "fields_accuracy": fields_accuracy,
            "extracted_fields": predicted_values
        }


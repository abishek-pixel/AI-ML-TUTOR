"""Responsible AI: bias detection, safety guardrails, and validation."""
from typing import Dict, List
import re

class ResponsibleAI:
    def __init__(self):
        self.bias_keywords = {
            'gender': ['he always', 'she always', 'men are', 'women are', 'boys are', 'girls are'],
            'stereotype': ['all', 'every', 'always', 'never', 'typically', 'usually'],
            'harmful': ['stupid', 'dumb', 'inferior', 'superior', 'primitive']
        }
        
        self.safety_filters = [
            'violence', 'weapon', 'harm', 'attack', 'kill', 'destroy',
            'illegal', 'hack', 'steal', 'fraud'
        ]
    
    def check_bias(self, text: str) -> Dict:
        """Check for potential biases in generated content."""
        text_lower = text.lower()
        detected_biases = {}
        bias_score = 0.0
        
        for bias_type, keywords in self.bias_keywords.items():
            found = []
            for keyword in keywords:
                if keyword in text_lower:
                    found.append(keyword)
                    bias_score += 0.1
            
            if found:
                detected_biases[bias_type] = found
        
        return {
            'has_bias': bool(detected_biases),
            'bias_types': detected_biases,
            'bias_score': min(1.0, bias_score),
            'severity': 'high' if bias_score > 0.5 else 'medium' if bias_score > 0.2 else 'low'
        }
    
    def check_hallucination(self, response: str, supporting_docs: List[str]) -> Dict:
        """Check if response contains unsupported claims (hallucinations)."""
        if not supporting_docs:
            return {
                'risk': 'high',
                'confidence': 0.0,
                'warning': 'No supporting documents found in knowledge base'
            }
        
        # Simple check: count factual statements vs supporting evidence
        sentences = re.split(r'[.!?]+', response)
        factual_sentences = [s for s in sentences if len(s.strip()) > 20]
        
        # Calculate coverage
        supported_count = 0
        for sentence in factual_sentences:
            for doc in supporting_docs:
                # Check if key terms from sentence appear in docs
                words = set(sentence.lower().split())
                doc_words = set(doc.lower().split())
                overlap = len(words & doc_words) / (len(words) + 1e-6)
                if overlap > 0.3:
                    supported_count += 1
                    break
        
        confidence = supported_count / (len(factual_sentences) + 1e-6)
        
        return {
            'risk': 'low' if confidence > 0.6 else 'medium' if confidence > 0.3 else 'high',
            'confidence': confidence,
            'warning': None if confidence > 0.6 else 'Some claims may not be fully supported'
        }
    
    def apply_safety_filter(self, text: str) -> Dict:
        """Apply content safety filters."""
        text_lower = text.lower()
        violations = []
        
        for filter_word in self.safety_filters:
            if filter_word in text_lower:
                violations.append(filter_word)
        
        return {
            'safe': len(violations) == 0,
            'violations': violations,
            'action': 'block' if violations else 'allow'
        }
    
    def add_disclaimer(self, response: str, confidence: float) -> str:
        """Add appropriate disclaimer based on confidence."""
        if confidence < 0.5:
            disclaimer = "\n\n⚠️ **Note:** This explanation may contain information not fully verified against the knowledge base. Please cross-reference with authoritative sources."
        elif confidence < 0.7:
            disclaimer = "\n\n**Note:** This explanation is generated with moderate confidence. Some details should be verified."
        else:
            disclaimer = ""
        
        return response + disclaimer
    
    def generate_report(self, term: str, response: str, supporting_docs: List[str]) -> str:
        """Generate comprehensive safety and quality report."""
        bias_check = self.check_bias(response)
        hallucination_check = self.check_hallucination(response, supporting_docs)
        safety_check = self.apply_safety_filter(response)
        
        report = f"### Responsible AI Report for '{term}'\n\n"
        
        report += f"**Bias Detection:**\n"
        report += f"- Bias Score: {bias_check['bias_score']:.2f}\n"
        report += f"- Severity: {bias_check['severity']}\n"
        if bias_check['detected_biases']:
            report += f"- Detected: {', '.join(bias_check['detected_biases'].keys())}\n"
        else:
            report += f"- No significant bias detected ✓\n"
        
        report += f"\n**Hallucination Risk:**\n"
        report += f"- Risk Level: {hallucination_check['risk']}\n"
        report += f"- Confidence: {hallucination_check['confidence']:.2%}\n"
        
        report += f"\n**Content Safety:**\n"
        report += f"- Status: {'✓ Safe' if safety_check['safe'] else '⚠ Flagged'}\n"
        
        return report

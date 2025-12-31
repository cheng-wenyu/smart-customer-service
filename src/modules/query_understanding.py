# src/query_understanding.py
class QueryUnderstanding:
    """智能Query理解模块"""
    
    def __init__(self):
        # 意图分类模型
        self.intent_classifier = self.load_intent_classifier()
        # 实体识别模型
        self.ner_model = self.load_ner_model()
    
    def process_query(self, query):
        """完整Query理解流程"""
        # 1. 意图识别
        intent = self.classify_intent(query)
        
        # 2. 实体提取
        entities = self.extract_entities(query)
        
        # 3. 查询重写
        rewritten_query = self.rewrite_query(query, intent, entities)
        
        # 4. 查询扩展
        expanded_queries = self.expand_query(rewritten_query)
        
        return {
            "original_query": query,
            "intent": intent,
            "entities": entities,
            "rewritten_query": rewritten_query,
            "expanded_queries": expanded_queries
        }

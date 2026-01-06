from infrastructure.models.ai_draft_order_model import AIDraftOrderModel

class AIDraftOrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_draft_from_voice(self, data):
        # Giả lập logic AI phân tích giọng nói thành văn bản
        recognized_text = data.get('voice_content', '')
        
        draft = AIDraftOrderModel(
            employee_id=data.get('employee_id'),
            customer_id=data.get('customer_id'),
            ai_id=1, # Giả sử dùng AI Assistant ID 1
            recognized_content=recognized_text,
            source="Voice",
            confirmation_status="Pending"
        )
        return self.repository.add(draft)
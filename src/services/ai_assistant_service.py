from infrastructure.models.ai_core.ai_assistant_model import AIAssistantModel

class AIAssistantService:
    def __init__(self, repository):
        # repository ở đây là AIAssistantRepository
        self.repository = repository

    def update_ai_settings(self, data):
        """
        Cấu hình thông số cho trợ lý AI (Version, Model type)
        """
        version = data.get('version', 'v1.0')
        model_type = data.get('model_type', 'GPT-3.5')

        # Logic: Bạn có thể kiểm tra nếu version trống thì báo lỗi
        if not version:
            raise ValueError("Phiên bản AI không được để trống")

        # Gọi repository để cập nhật vào database
        return self.repository.update_config(version, model_type)

    def get_current_config(self):
        """Lấy cấu hình AI hiện tại"""
        return self.repository.get_latest_config()
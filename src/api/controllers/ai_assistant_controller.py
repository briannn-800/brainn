from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.ai_assistant_service import AIAssistantService
from infrastructure.repositories.ai_assistant_repository import AIAssistantRepository
from infrastructure.databases.mssql import session

ai_assistant_bp = Blueprint('ai_assistant_bp', __name__)

# Khởi tạo đúng quy trình
ai_repo = AIAssistantRepository(session)
ai_service = AIAssistantService(ai_repo)

@ai_assistant_bp.route('/config', methods=['POST'])
@token_required
def config_ai_version():
    """
    Cấu hình phiên bản AI
    ---
    tags: [AI Features]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            version: {type: string, example: "v2.0"}
            model_type: {type: string, example: "GPT-4o"}
    responses:
      200: {description: "Cấu hình thành công"}
    """
    try:
        data = request.get_json()
        ai_service.update_ai_settings(data)
        return jsonify({"message": "Cấu hình AI đã được cập nhật"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
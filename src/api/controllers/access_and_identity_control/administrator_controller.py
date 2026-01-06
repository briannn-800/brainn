from flask import Blueprint, request, jsonify
from infrastructure.repositories.access_and_identity_repo.administrator_repository import AdministratorRepository
from services.access_and_identity_service.administrator_service import AdministratorService
from infrastructure.databases.mssql import session

admin_bp = Blueprint('admin_bp', __name__)

# Khởi tạo đúng dây chuyền
admin_repo = AdministratorRepository(session)
admin_service = AdministratorService(admin_repo)

# ... (Phần import giữ nguyên)

@admin_bp.route('/', methods=['POST'])
def create():
    """
    Tạo Admin mới
    ---
    tags: [Administrators]
    parameters:
      - in: body
        name: body
        schema:
          required: [admin_name, password]
          properties:
            admin_name: {type: string, example: "admin_test"}
            password: {type: string, example: "123456"}
            admin_permission: {type: string, example: "Full"}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = admin_service.create_admin(data)
        return jsonify({"message": "Thành công", "id": result.admin_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... (giữ nguyên phần khởi tạo trên đầu)

@admin_bp.route('/', methods=['GET'])
def list_admins():
    """
    Lấy danh sách Admin
    ---
    get:
      tags: [Administrators]
      responses:
        200:
          description: Thành công
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AdministratorResponse'
    """
    try:
        admins = admin_service.get_all_admins() # Cần thêm hàm này trong Service/Repo
        return jsonify([{"id": a.admin_id, "name": a.admin_name} for a in admins]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
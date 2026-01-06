from flask import Blueprint, request, jsonify
from services.access_and_identity_service.employee_service import EmployeeService
from infrastructure.repositories.access_and_identity_repo.employee_repository import EmployeeRepository
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required

employee_bp = Blueprint('employee_bp', __name__)

emp_repo = EmployeeRepository(session)
emp_service = EmployeeService(emp_repo)

@employee_bp.route('/', methods=['POST'])
@token_required
def create_new_employee(): # Tên hàm duy nhất tránh AssertionError
    """
    Tạo nhân viên mới
    ---
    tags: [Employees]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [employee_name, owner_id, password]
          properties:
            employee_name: {type: string, example: "Nguyen Van Employee"}
            role: {type: string, example: "Staff"}
            password: {type: string, example: "123456"}
            owner_id: {type: integer, example: 1}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = emp_service.create_employee(data)
        return jsonify({"message": "Thành công", "id": result.employee_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_bp.route('/owner/<int:owner_id>', methods=['GET'])
@token_required
def list_employees_by_owner(owner_id):
    """
    Lấy danh sách nhân viên của một chủ sở hữu
    ---
    tags: [Employees]
    security: [{BearerAuth: []}]
    parameters:
      - name: owner_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Thành công
    """
    try:
        employees = emp_service.get_employees_by_owner(owner_id)
        return jsonify([
            {
                "id": e.employee_id, 
                "name": e.employee_name, 
                "role": e.role,
                "status": e.active_status
            } for e in employees
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#from api.controllers.todo_controller import bp as todo_bp
from api.controllers.business_owner_controller import business_owner_bp
from api.controllers.employee_controller import employee_bp
from api.controllers.product_controller import product_bp
from api.controllers.administrator_controller import admin_bp
from api.controllers.customer_controller import customer_bp
from api.controllers.subscription_plan_controller import subscription_plan_bp
from api.controllers.unit_controller import unit_bp
from api.controllers.order_controller import order_bp
from api.controllers.order_detail_controller import order_detail_bp
from api.controllers.debt_controller import debt_bp
from api.controllers.payment_controller import payment_bp
from api.controllers.account_report_controller import account_report_bp
from api.controllers.ai_assistant_controller import ai_assistant_bp
from api.controllers.ai_draft_order_controller import ai_draft_order_bp
from api.controllers.auth_controller import auth_bp






def register_routes(app):
    # Đăng ký todo ở đây (vì đã xóa ở app.py)
    #app.register_blueprint(todo_bp, url_prefix='/todos')
    # Đăng ký Business Owner
    app.register_blueprint(business_owner_bp, url_prefix='/business-owners')


    app.register_blueprint(employee_bp, url_prefix='/employees')

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(admin_bp, url_prefix='/administrators')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(subscription_plan_bp, url_prefix='/subscription-plans')

    app.register_blueprint(unit_bp, url_prefix='/units')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(order_detail_bp, url_prefix='/order-details')
    app.register_blueprint(debt_bp, url_prefix='/debts')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(account_report_bp, url_prefix='/account-reports')
    app.register_blueprint(ai_assistant_bp, url_prefix='/ai-assistants')
    app.register_blueprint(ai_draft_order_bp, url_prefix='/ai-draft-orders')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    










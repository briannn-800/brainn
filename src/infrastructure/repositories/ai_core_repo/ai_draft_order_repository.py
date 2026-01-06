from infrastructure.models.ai_core.ai_draft_order_model import AIDraftOrderModel
from domain.models.ai_draft_order import AIDraftOrder
from infrastructure.databases.mssql import session

class AIDraftOrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, draft: AIDraftOrder):
        try:
            db_draft = AIDraftOrderModel(
                employee_id=draft.employee_id,
                ai_id=draft.ai_id,
                customer_id=draft.customer_id,
                recognized_content=draft.recognized_content,
                confirmation_status=draft.confirmation_status,
                source=draft.source
            )
            self.session.add(db_draft)
            self.session.commit()
            self.session.refresh(db_draft)
            return db_draft
        except Exception as e:
            self.session.rollback()
            raise e
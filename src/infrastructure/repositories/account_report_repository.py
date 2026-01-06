from infrastructure.models.account_report_model import AccountReportModel
from infrastructure.databases.mssql import session

class AccountReportRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, report_model):
        try:
            self.session.add(report_model)
            self.session.commit()
            self.session.refresh(report_model)
            return report_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_owner(self, owner_id):
        return self.session.query(AccountReportModel).filter_by(owner_id=owner_id).all()
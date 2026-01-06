from datetime import date
from infrastructure.models.account_report_model import AccountReportModel

class AccountReportService:
    def __init__(self, repository):
        self.repository = repository

    def create_report(self, data):
        # Logic tạo báo cáo (ví dụ: mặc định lấy ngày hiện tại)
        new_report = AccountReportModel(
            owner_id=data['owner_id'],
            report_type=data.get('report_type', 'Daily'),
            report_name=data.get('report_name', f"Report-{date.today()}"),
            generated_date=date.today()
        )
        return self.repository.add(new_report)

    def get_owner_reports(self, owner_id):
        return self.repository.get_by_owner(owner_id)
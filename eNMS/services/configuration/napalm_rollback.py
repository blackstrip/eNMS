from sqlalchemy import Boolean, ForeignKey, Integer
from wtforms import HiddenField

from eNMS.database.dialect import Column, MutableDict, SmallString
from eNMS.forms.automation import ConnectionForm, ServiceForm
from eNMS.forms.services import NapalmForm
from eNMS.models.automation import ConnectionService


class NapalmRollbackService(ConnectionService):

    __tablename__ = "napalm_rollback_service"
    pretty_name = "NAPALM Rollback"

    id = Column(Integer, ForeignKey("connection_service.id"), primary_key=True)
    driver = Column(SmallString)
    use_device_driver = Column(Boolean, default=True)
    timeout = Column(Integer, default=60)
    optional_args = Column(MutableDict)

    __mapper_args__ = {"polymorphic_identity": "napalm_rollback_service"}

    def job(self, run, payload, device):
        napalm_connection = run.napalm_connection(device)
        run.log("info", f"Configuration rollback on {device.name} (Napalm)")
        napalm_connection.rollback()
        return {"success": True, "result": "Rollback successful"}


class NapalmRollbackForm(ServiceForm, ConnectionForm, NapalmForm):
    form_type = HiddenField(default="napalm_rollback_service")
    groups = {
        "Napalm Parameters": NapalmForm.group,
        "Connection Parameters": ConnectionForm.group,
    }

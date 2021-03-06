
# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component
from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import datetime
import logging
import json

_logger = logging.getLogger(__name__)


class Service(Component):
    _inherit = "base.rest.service"
    _name = "judged.service"
    _usage = "Judged"
    _collection = "base.rest.csj.odoo.private.services"
    _description = """
        Judged Services
        Access to the Judged services is only allowed to authenticated partners.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Obtener Información de un Juzgado
        """
        partner = self.env["res.partner"].browse(_id)
        return self._to_json(partner)

    def search(self, name):
        """
        Buscar Juzgados por Nombre
        """

        partners = self.env["res.partner"].name_search(name)
        partners = self.env["res.partner"].search([('name','ilike',name),('company_type', '=', 'judged')])
        rows = []
        res = {"count": len(partners), "rows": rows}
        for partner in partners:
            _logger.error('--------------------------partners----------------------')
            _logger.error(partner)
            rows.append(self._to_json(partner))
        return res


    def _get(self, _id):
        return self.env["res.partner"].browse(_id)

    def _get_document(self, _id):
        return self.env["res.partner"].browse(_id)

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "string", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}


    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_create(self):
        res = {

            "name": {"type": "string", "required": True, "empty": False},
            "code": {"type": "string", "required": False, "empty": True},
            "office": {"type": "string", "required": False, "empty": True},
            "entity_name": {"type": "string", "required": False, "empty": True},
            "specialty_name": {"type": "string", "required": False, "empty": True},
            #"ext_lifesize": {"type": "string", "required": False, "empty": True}
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, partner):
        res = {
            "id": partner.judged_only_code,
            "name": partner.name,
            "code": partner.code,
            "office": partner.mame,
            "entity_name": partner.entity_id.name,
            "specialty_name": partner.specialty_id.name,
            #"ext_lifesize": partner.extension_lifesize
        }
        return res

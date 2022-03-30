# -*- coding: utf-8 -*-


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    consignee_company_ids = fields.Many2many(related='company_id.consignee_company_ids', string="Consignee's Company ", readonly=False)
    source_location_id = fields.Many2one(related='company_id.source_location_id', readonly=False)
    dest_location_id = fields.Many2one(related='company_id.dest_location_id', readonly=False)
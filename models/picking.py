# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime

class Move(models.Model):
    _inherit = "stock.move"
    used_quants = fields.Char()

class Picking(models.Model):
    _inherit = "stock.picking"

    is_dc_transfer = fields.Boolean()

    def action_check_current_onhand(self):
        """
        To check on hand before validating
        """
        for rec in self:
            for move in rec.move_ids_without_package:
                quant = self.env['stock.quant'].browse(int(move.used_quants))
                if move.product_uom_qty != quant.available_quantity:
                    move.update({'product_uom_qty': quant.available_quantity})


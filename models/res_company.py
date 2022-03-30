# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime

class ResCompany(models.Model):
    _inherit = "res.company"


    consignee_company_ids = fields.Many2many('res.company','company_company_config_rel','config_company_id', 'comp_company_id', string="Consignee's Company ", readonly=False)
    source_location_id = fields.Many2one('stock.location', string='Location')
    dest_location_id = fields.Many2one('stock.location', string='Destination Location')

    def check_weekend_for_picking(self, picking):
        """
        To update scheduled date if its weekend it will take next working day
        :param picking:
        """
        picking.scheduled_date = picking.scheduled_date + datetime.timedelta(days=1)
        if picking.scheduled_date.weekday() >= 5:
            self.check_weekend_for_picking(picking)


    def update_stock(self):
        for comp in self:
            ctx = dict(self.env.context)
            picking_vals = {}
            source_location = self.env.company.source_location_id
            dest_location = self.env.company.dest_location_id.id
            comp = ctx.get('comp_check')
            quants  = self.env['stock.quant'].search([('owner_id', '=', comp.partner_id.id),('location_id', '=', source_location.id),('location_id.usage', '=', 'internal')])
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'internal'), ('company_id', '=',comp.id)], limit=1)
            picking_vals.update(
                {'state': 'draft', 'company_id': ctx.get('comp_check').id,
                 'is_dc_transfer': True})
            if picking_type:
                picking_vals.update(
                    {'picking_type_id': picking_type.id})
            lines = []
            for rec in quants:
                lines.append((0, 0, {
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.available_quantity,
                    'name': 'B',
                    'used_quants': rec.id,
                    'product_uom': rec.product_id.uom_id.id,
                }))
            if source_location and dest_location:
                picking_vals.update({'move_ids_without_package': lines, 'location_id': source_location.id, 'location_dest_id': dest_location,
                                     'name': picking_type.sequence_id.next_by_id()})
                new_picking = self.env['stock.picking'].sudo().create(picking_vals)
                if new_picking.company_id.id != ctx.get('comp_check').id:
                    new_picking.sudo().write({'company_id':  ctx.get('comp_check').id})
                if new_picking.scheduled_date.weekday() >= 5:
                    self.check_weekend_for_picking(new_picking)

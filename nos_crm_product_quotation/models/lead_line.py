# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _


class LeadLine(models.Model):
    _name = 'lead.line'
    _description = "Lead Line"

    lead_line_id = fields.Many2one('crm.lead', string="CRM Lead", ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Text(string='Description', required=True)
    product_uom_quantity = fields.Float(
        string='Order Quantity', 
        digits='Product Unit of Measure', 
        required=True, 
        default=1.0
    )
    product_uom = fields.Many2one(
        'uom.uom', 
        string='Unit of Measure',
        domain="[('category_id', '=', product_uom_category_id)]"
    )
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float('Unit Price', default=0.0)
    tax_id = fields.Many2many('account.tax', string='Taxes')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.product_uom = self.product_id.uom_id.id


class CrmPurchaseLine(models.Model):
    _name = 'crm.purchase.line'
    _description = 'CRM Purchase Line'

    lead_pro_id = fields.Many2one('crm.lead', string='Lead', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Vendor")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_qty = fields.Float(string="Quantity", required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", required=True)
    price_unit = fields.Float(string="Unit Price", required=True)
    name = fields.Char(string="Description", required=True)
    date_planned = fields.Datetime(string="Planned Date", default=fields.Datetime.now)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.name = self.product_id.name
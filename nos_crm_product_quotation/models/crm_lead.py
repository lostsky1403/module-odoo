# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import itertools
import operator
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class purchase_or(models.Model):
    _inherit = 'purchase.order'

    pu_ord_id = fields.Many2one('crm.lead')

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    lead_product_ids = fields.One2many('lead.line', 'lead_line_id', string='Products', copy=True)
    crm_count = fields.Integer(string="Quotation",compute="get_quotation_count")
    is_crm_quotation = fields.Boolean('Is CRM Quotation')
    purchase_line_ids = fields.One2many('crm.purchase.line', 'lead_pro_id')
    po_flags = fields.Boolean(string='po flag', copy=False)
    po_ids = fields.One2many('purchase.order', 'pu_ord_id', string='Purchase')
    po_count = fields.Integer(string='PO Orders', compute='_compute_picking_ids')

    @api.depends('po_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.po_count = len(order.po_ids)

    def create_purchase_order(self):
        if not self.purchase_line_ids:
            raise UserError(_('Please add Purchase Quotation Line Products'))
        po_id = []
        line_ids = self._context.get('active_ids')
        vals = []
        for lead in self:
            for line in lead.purchase_line_ids:
                if line.partner_id:
                    vals.append({
                        'partner_id': line.partner_id.id or '',
                        'product_id': line.product_id.id or '',
                        'product_qty': line.product_qty,
                        'product_uom': line.uom_id.id,
                        'price_unit': line.price_unit,
                        'name': line.name,
                        'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    })
            res = sorted(vals, key=operator.itemgetter('partner_id'))
            groups = itertools.groupby(res, key=operator.itemgetter('partner_id'))
            par_group = [{'partner_id': k, 'values': [x for x in v]} for k, v in groups]
            for vals in par_group:
                purchase_id = self.env['purchase.order'].create({'partner_id': vals['partner_id']})
                po_id.append(purchase_id.id)
                for line_val in vals['values']:
                    res = {
                        'product_id': line_val['product_id'],
                        'product_qty': line_val['product_qty'],
                        'product_uom': line_val['product_uom'],
                        'price_unit': line_val['price_unit'],
                        'name': line_val['name'],
                        'date_planned': line_val['date_planned'],
                        'order_id': purchase_id.id,
                    }
                    self.env['purchase.order.line'].create(res)

            if self.po_flags == True:
                raise UserError(_('Purchase Quotations already exist for this Opportunity'))
            self.write({'po_flags': True})

        self.po_ids = po_id

        return {
            'domain': [('id', 'in', po_id)],
            'view_mode': 'tree,form',
            'res_id': purchase_id.id,
            'res_model': 'purchase.order',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
        }
    def purchase_order_status(self):
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        po_ids = self.mapped('po_ids')
        if len(po_ids) > 1:
            action['domain'] = [('id', 'in', po_ids.ids)]
        elif po_ids:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = po_ids.id
        return action

    def action_quotations_view(self):
        order_line = [] 
        for record in self.lead_product_ids:  
            order_line.append((0, 0, {
                                     'product_id'     : record.product_id.id,
                                     'name'           : record.name, 
                                     'product_uom_qty': record.product_uom_quantity,
                                     'price_unit'     : record.price_unit,
                                     'tax_id'        : [(6, 0, record.tax_id.ids)],
                                }))
        
        sale_obj = self.env['sale.order']
        if self.partner_id:
            for record in self.lead_product_ids:  
                if record.product_id and record.name:
                    sale_create_obj = sale_obj.create({
                                    'partner_id': self.partner_id.id,
                                    'opportunity_id': self.id,
                                    'state': "draft",
                                    'order_line': order_line,
                                    })
                return {
                    'name': "Sale Order",
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': self.env.ref('sale.view_order_form').id,
                    'target': "new",
                    'res_id': sale_create_obj.id
                }
            else:
                raise UserError('Enter the "Product" and "Description".')
        else:
            raise UserError('Please select the "Customer".')             



    def open_quotation_from_view_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['domain'] = [('partner_id','=',self.partner_id.id),('opportunity_id','=',self.id)]
        return action


    def get_quotation_count(self):
        count = self.env['sale.order'].search_count([('partner_id','=',self.partner_id.id),('opportunity_id','=',self.id)])
        self.crm_count = count

    def generate_purchase_lines(self):
        for lead in self:
            # Clear existing purchase lines
            lead.purchase_line_ids.unlink()
            purchase_lines = []
            for product in lead.lead_product_ids:
                purchase_lines.append((0, 0, {
                    'product_id': product.product_id.id,
                    'product_qty': product.product_uom_quantity,
                    'price_unit': product.price_unit,
                    'name': product.name,
                    'uom_id': product.product_uom.id if product.product_uom else False,
                }))
            lead.write({'purchase_line_ids': purchase_lines})



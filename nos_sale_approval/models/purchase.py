# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[
        ('purchase_approval', 'Waiting Purchase Approval'),
        ('director_approval', 'Waiting Director Approval'),
        ('refuse', 'Refuse')],
        string='Status',
    )

    request_approve_id = fields.Many2one(
        'res.users',
        string='Request Approval',
        readonly=True,
    )
    approve_purchase_manager_id = fields.Many2one(
        'res.users',
        string='Approve Purchase Manager',
        readonly=True,
    )
    approve_director_manager_id = fields.Many2one(
        'res.users',
        string='Approve Director Manager',
        readonly=True,
    )
    request_approve_date = fields.Datetime(
        string='Request Approval Date',
        readonly=True,
    )
    purchase_manager_approve_date = fields.Datetime(
        string='Purchase Manager Approve Date',
        readonly=True,
    )
    director_manager_approve_date = fields.Datetime(
        string='Director Manager Approve Date',
        readonly=True,
    )
    req_approval_po = fields.Boolean(string='request approval')

    def button_req_approve(self):
        self.write({'state': 'purchase_approval',
                    'req_approval_po': True,
                    'request_approve_id': self.env.user.id,
                    'request_approve_date': fields.Datetime.now()})

    def button_purchase_approval(self):
        for order in self:
            order.write({'state': 'sent',
                         'approve_purchase_manager_id':self.env.user.id,
                         'purchase_manager_approve_date':fields.Datetime.now()
                         })
        return True

    def button_director_approval(self):
        for order in self:
            order.write({'approve_director_manager_id': self.env.user.id,
                         'director_manager_approve_date': fields.Datetime.now()
                         })
        return super(PurchaseOrder, self).button_confirm()
    #
    # def button_confirm(self):
    #     for order in self:
    #         if order.state not in ['draft', 'sent', 'director_approval']:
    #             continue
    #     return super(PurchaseOrder, self).button_confirm()

    # def button_confirm(self):
    #     for order in self:
    #         if order.state not in ['draft', 'sent', 'finance_approval', 'director_approval']:
    #             continue
    #         order.order_line._validate_analytic_distribution()
    #         order._add_supplier_to_product()
    #         # Deal with double validation process
    #         if order._approval_allowed():
    #             order.button_approve()
    #         else:
    #             order.write({'state': 'to approve'})
    #         if order.partner_id not in order.message_partner_ids:
    #             order.message_subscribe([order.partner_id.id])
    #     return True




    def disapprove_purchase(self):
        for order in self:
            order.write({'state': 'cancel',
                         'req_approval_po': False,
                         })

# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[
            ('purchase_approval', 'Waiting Purchase Approval'),
            ('director_approval', 'Waiting Director Approval'),
            ('refuse', 'Refuse')
        ],
        string='Status',
        ondelete={
            'purchase_approval': 'set default',
            'director_approval': 'set default',
            'refuse': 'set default'
        }
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
    req_approval_po = fields.Boolean(string='Request Approval')

    def button_req_approve(self):
        self.write({
            'state': 'purchase_approval',
            'req_approval_po': True,
            'request_approve_id': self.env.user.id,
            'request_approve_date': fields.Datetime.now()
        })

    def button_purchase_approval(self):
        for order in self:
            order.write({
                'state': 'sent',
                'approve_purchase_manager_id': self.env.user.id,
                'purchase_manager_approve_date': fields.Datetime.now()
            })
        return True

    def button_director_approval(self):
        for order in self:
            order.write({
                'approve_director_manager_id': self.env.user.id,
                'director_manager_approve_date': fields.Datetime.now()
            })
        return super().button_confirm()

    def disapprove_purchase(self):
        for order in self:
            order.write({
                'state': 'cancel',
                'req_approval_po': False,
            })
# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('state')
    def _custom_set_sale_user(self):
        for rec in self:
            if rec.state in ('draft', 'sent'):
                rec.custom_sale_user_id = self.env.user.id

    state = fields.Selection(
        selection_add=[
            ('director_approval', 'Waiting Director Approval'),
            ('refuse', 'Refuse')
        ],
        string='Status',
        ondelete={'director_approval': 'set default', 'refuse': 'set default'}
    )
    
    so_refuse_user_id = fields.Many2one(
        'res.users',
        string="Refused By",
        readonly=True,
    )
    so_refuse_date = fields.Date(
        string="Refused Date",
        readonly=True
    )
    refuse_reason_note = fields.Text(
        string="Refuse Reason",
        readonly=True
    )
    request_approve_id = fields.Many2one(
        'res.users',
        string='Request Approval',
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
    director_manager_approve_date = fields.Datetime(
        string='Director Manager Approve Date',
        readonly=True,
    )
    custom_sale_user_id = fields.Many2one(
        'res.users',
        string='Sale User',
        compute='_custom_set_sale_user',
        store=True,
    )
    req_approval = fields.Boolean(string='Request Approval')

    def button_req_approve(self):
        self.write({
            'state': 'director_approval',
            'req_approval': True,
            'request_approve_id': self.env.user.id,
            'request_approve_date': fields.Datetime.now()
        })

    def button_director_approval(self):
        for order in self:
            order.write({
                'approve_director_manager_id': self.env.user.id,
                'director_manager_approve_date': fields.Datetime.now()
            })
        return super().action_confirm()

    def _can_be_confirmed(self):
        """This function _can_be_confirmed adds waiting state"""
        self.ensure_one()
        return self.state in {'draft', 'sent', 'director_approval'}

    def button_reset_to_draft(self):
        for order in self:
            if order.state == 'refuse':
                order.write({'state': 'draft'})

    def _get_so_refuse_template_id(self):
        """Get refuse email template"""
        return self.env.ref('nos_sale_approval.email_template_sale_refuse', raise_if_not_found=False)
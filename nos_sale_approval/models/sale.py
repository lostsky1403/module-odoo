# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('state')
    def _custom_set_sale_user(self):
        for rec in self:
            if rec.state == 'draft' or 'sent':
                rec.custom_sale_user_id = self.env.user.id,

    state = fields.Selection(selection_add=[
        # ('finance_approval', 'Waiting Finance Approval'),
        ('director_approval', 'Waiting Director Approval'),
        ('refuse', 'Refuse')],
        string='Status',
    )
    so_refuse_user_id = fields.Many2one(
        'res.users',
        string="Refused By",
        readonly = True,
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
    # approve_finance_manager_id = fields.Many2one(
    #     'res.users',
    #     string='Approve Finance Manager',
    #     readonly=True,
    # )
    approve_director_manager_id = fields.Many2one(
        'res.users',
        string='Approve Director Manager',
        readonly=True,
    )
    request_approve_date = fields.Datetime(
        string='Request Approval Date',
        readonly=True,
    )
    # finance_manager_approve_date = fields.Datetime(
    #     string='Finance Manager Approve Date',
    #     readonly=True,
    # )
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
    req_approval = fields.Boolean(string='request_approval')

    def button_req_approve(self):
        self.write({'state': 'director_approval',
                    'req_approval': True,
                    'request_approve_id': self.env.user.id,
                    'request_approve_date': fields.Datetime.now()})

    # def button_finance_approval(self):
    #     for order in self:
    #         order.write({'state': 'director_approval',
    #                      'approve_finance_manager_id':self.env.user.id,
    #                      'finance_manager_approve_date':fields.Datetime.now()
    #                      })
    #     return True

    def button_director_approval(self):
        for order in self:
            order.write({'approve_director_manager_id': self.env.user.id,
                         'director_manager_approve_date': fields.Datetime.now()
                         })
        return super().action_confirm()

    def _can_be_confirmed(self):
        """This function _can_be_confirmed adds waiting state """
        self.ensure_one()
        # return self.state in {'draft', 'sent', 'finance_approval', 'director_approval'}
        return self.state in {'draft', 'sent', 'director_approval'}

    # def button_director_approval(self):
    #     super(SaleOrder, self).action_confirm()
    #     return


    def button_reset_to_draft(self):
        for order in self:
            if order.state in ['refuse']:
                order.action_confirm()


# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrderRefuseWizard(models.TransientModel):
    _name = 'sale.order.refuse.wizard'
    _description = "Refuse Sale Order"

    note = fields.Text(
        string="Refuse Reason",
        required=True,
    )

    def action_so_refuse(self):
        sale_order_id = self.env['sale.order'].browse(int(self._context.get('active_id')))
        for rec in self:
            sale_order_id.refuse_reason_note = rec.note
            sale_order_id.so_refuse_user_id = rec.env.uid
            sale_order_id.so_refuse_date = fields.Date.today()
            so_refuse_template_id = sale_order_id._get_so_refuse_template_id()
            ctx = self._context.copy()
            if sale_order_id.state == 'director_approval':
                ctx.update({
                    'name': sale_order_id.create_uid.partner_id.name,
                    'email_to': sale_order_id.create_uid.partner_id.email,
                    'subject': _('Sale Order: ') + sale_order_id.name + _(' Refused'),
                    'manager_name': _('Director: ') + sale_order_id.director_manager_id.name,
                    'reason': rec.note,
                    })
            if so_refuse_template_id and sale_order_id.state in ['to_request', 'finance_approval', 'director_approval']:
                so_refuse_template_id.with_context(ctx).send_mail(sale_order_id.id)
            sale_order_id.state = 'refuse'

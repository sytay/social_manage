from odoo import models, fields, api


class MailChannelInherit(models.Model):


    _inherit = 'mail.channel'

    facebook_PSID = fields.Char()
    social_account_id = fields.Many2one('social.account')

    def message_post(self, message_type='notification', **kwargs):
        message = super(MailChannelInherit, self).message_post(message_type='notification', **kwargs)

        return message

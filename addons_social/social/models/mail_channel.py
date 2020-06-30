from odoo import models, fields, api
import requests
import logging
import json

class MailChannelInherit(models.Model):


    _inherit = 'mail.channel'

    facebook_PSID = fields.Char()
    social_account_id = fields.Many2one('social.account')

    def message_post(self, message_type='notification', **kwargs):
        message = super(MailChannelInherit, self).message_post(message_type='notification', **kwargs)

        if self.facebook_PSID and not kwargs.get("webhook"):
            message_obj = {
                "messaging_type": "RESPONSE",
                "recipient": {
                    "id": self.facebook_PSID
                },
                "message": {
                    "text": kwargs.get('body')
                }
            }
            headers = {
                "Content-Type": "application/json"
            }
            access_token = self.social_account_id.facebook_access_token
            url = "https://graph.facebook.com/v6.0/me/messages?access_token={access_token}".format(
                access_token=access_token)

            try:
                response = requests.post(url, headers=headers, data=json.dumps(message_obj))
            except Exception as e:

                logging.error("Khong gui duoc tin nhan")

        return message

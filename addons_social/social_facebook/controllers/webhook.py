from odoo import http
from odoo.http import request
import logging
import json

class FacebookWebhook(http.Controller):

    @http.route(['/webhook'], type='http',method=['POST','GET'],csrf=False,auth='public')
    def webhook(self,**kwargs):
        if  request.httprequest.method == 'GET':
            return self.check_webhook(kwargs)
        else:
            self.receive_message(json.loads(request.httprequest.data.decode('utf-8')))
            return 'ok'

    def check_webhook(self,data):
        if data.get('hub.mode') == 'subscribe':
            return data.get('hub.challenge')
        return 'fail'

    def receive_message(self,data):
        logging.info(data)

        Channel = http.request.env["mail.channel"].sudo()

        facebook_messaging = data.get('entry')[0].get('messaging')[0]
        facebook_PSID = facebook_messaging.get('sender').get('id')
        facebook_page_id = facebook_messaging.get('recipient').get('id')
        message = facebook_messaging.get('message').get('text')

        channel = Channel.sudo().search([('facebook_PSID','=',facebook_PSID)],limit=1)
        if not channel.id:
            social_account = http.request.env["social.account"].sudo().search([('facebook_account_id','=',facebook_page_id)],limit=1)
            channel = Channel.sudo().create({
                'public': 'public',
                'email_send': False,
                'channel_type': 'chat',
                'facebook_PSID': facebook_PSID,
                'social_account_id': social_account.id,
                'name': 'facebook chat',
            })
        channel.message_post(message_type='comment', partner_ids=[], body=message, attachment_ids=[],
							  canned_response_ids=[], subtype='mail.mt_comment', webhook=True)





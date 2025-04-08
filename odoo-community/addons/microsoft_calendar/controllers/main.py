# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.calendar.controllers.main import CalendarController


class MicrosoftCalendarController(CalendarController):

    @http.route('/microsoft_calendar/sync_data', type='json', auth='user')
    def microsoft_calendar_sync_data(self, model, **kw):
        """ This route/function is called when we want to synchronize Odoo
            calendar with Microsoft Calendar.
            Function return a dictionary with the status :  need_config_from_admin, need_auth,
            need_refresh, sync_stopped, success if not calendar_event
            The dictionary may contains an url, to allow Odoo Client to redirect user on
            this URL for authorization for example
        """
        if model == 'calendar.event':
            MicrosoftCal = request.env["calendar.event"]._get_microsoft_service()

            # Checking that admin have already configured Microsoft API for microsoft synchronization !
            client_id = request.env['ir.config_parameter'].sudo().get_param('microsoft_calendar_client_id')

            if not client_id or client_id == '':
                action_id = ''
                if MicrosoftCal._can_authorize_microsoft(request.env.user):
                    action_id = request.env.ref('base_setup.action_general_configuration').id
                return {
                    "status": "need_config_from_admin",
                    "url": '',
                    "action": action_id
                }

            # Checking that user have already accepted Odoo to access his calendar !
            if not MicrosoftCal.is_authorized(request.env.user):
                url = MicrosoftCal._microsoft_authentication_url(from_url=kw.get('fromurl'))
                return {
                    "status": "need_auth",
                    "url": url
                }

            # If App authorized, and user access accepted, We launch the synchronization
            need_refresh = request.env.user.sudo().with_context(dont_notify=True)._sync_microsoft_calendar()

            # If synchronization has been stopped or paused
            sync_status = request.env.user._get_microsoft_sync_status()
            if not need_refresh and sync_status != "sync_active":
                return {
                    "status": sync_status,
                    "url": ''
                }
            return {
                "status": "need_refresh" if need_refresh else "no_new_event_from_microsoft",
                "url": ''
            }

        return {"status": "success"}

# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super().session_info()

        if self.env.user.has_group('base.group_user'):
            user = request.env.user

            session_info.update({
                "user_branches": {
                    'current_branch': user.branch_id.id,
                    'allowed_branches': {
                        branch.id: {
                            "id": branch.id,
                            "name": branch.name
                        } for branch in user.branch_ids
                    },
                },
                "display_switch_branch_menu": user.has_group('branch.group_multi_branch') and len(user.branch_ids) > 1
            })

        return session_info

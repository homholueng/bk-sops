# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging

from auth_backend.plugins.utils import search_all_resources_authorized_actions

from gcloud.conf import settings
from gcloud.core.utils import get_user_business_list
from gcloud.core.models import Business, Project, UserDefaultProject
from gcloud.core.permissions import project_resource

logger = logging.getLogger("root")

CACHE_PREFIX = __name__.replace('.', '_')
DEFAULT_CACHE_TIME_FOR_CC = settings.DEFAULT_CACHE_TIME_FOR_CC
get_client_by_user = settings.ESB_GET_CLIENT_BY_USER


def sync_projects_from_cmdb(username, use_cache=True):
    biz_list = get_user_business_list(username=username, use_cache=use_cache)
    business_dict = {}

    for biz in biz_list:
        if biz['bk_biz_name'] == u"资源池":
            continue
        defaults = {
            'cc_name': biz['bk_biz_name'],
            'cc_owner': biz['bk_supplier_account'],
            'cc_company': biz.get('bk_supplier_id') or 0,
            'time_zone': biz.get('time_zone', ''),
            'life_cycle': biz.get('life_cycle', ''),
            'status': biz.get('bk_data_status', 'enable')
        }

        # update or create business obj
        Business.objects.update_or_create(
            cc_id=biz['bk_biz_id'],
            defaults=defaults
        )

        business_dict[biz['bk_biz_id']] = {
            'cc_name': defaults['cc_name'],
            'time_zone': defaults['time_zone'],
            'creator': username
        }

    # sync projects from business
    Project.objects.sync_project_from_cmdb_business(business_dict)


def get_default_project_for_user(username):
    project = None
    try:
        project = UserDefaultProject.objects.get(username=username).default_project
    except UserDefaultProject.DoesNotExist:
        resources_perms = search_all_resources_authorized_actions(username, project_resource.rtype, project_resource,
                                                                  action_ids=[project_resource.actions.view.id])
        if resources_perms:
            project = Project.objects.filter(id__in=resources_perms.keys()).first()
    return project

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

import sys
import logging
import traceback

from django.apps import AppConfig
from django.db.utils import ProgrammingError

from pipeline.conf import settings

logger = logging.getLogger('root')


class ExternalPluginsConfig(AppConfig):
    name = 'pipeline.contrib.external_plugins'

    def ready(self):
        from pipeline.contrib.external_plugins import loader  # noqa
        from pipeline.contrib.external_plugins.models import ExternalPackageSource  # noqa

        if not sys.argv[1:2] == ['test']:
            try:
                logger.info('Start to update package source from config file...')
                ExternalPackageSource.update_package_source_from_config(getattr(settings,
                                                                                'COMPONENTS_PACKAGE_SOURCES',
                                                                                {}))
            except ProgrammingError as e:
                logger.warning('update package source failed, maybe first migration? exception: %s' %
                               traceback.format_exc())
                # first migrate
                return

            logger.info('Start to load external modules...')

            loader.load_external_modules()

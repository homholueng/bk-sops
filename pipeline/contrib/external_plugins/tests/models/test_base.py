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

from django.test import TestCase

from pipeline.contrib.external_plugins import exceptions
from pipeline.contrib.external_plugins.models import GitRepoSource

SOURCE_NAME = 'source_name'
PACKAGES = [{'1': 1}, {'2': 2}]
FROM_CONFIG = True
REPO_RAW_ADDRESS = 'REPO_RAW_ADDRESS'
BRANCH = 'master'

OLD_SOURCE_1 = {
    'name': 'source_1',
    'details': {
        'repo_raw_address': 'old_address',
        'branch': 'stage',
    },
    'packages': {
        'root_package': {
            'version': '',
            'modules': ['test1']
        }
    }
}

OLD_SOURCE_3 = {
    'name': 'source_3',
    'details': {
        'repo_raw_address': 'old_address_3',
        'branch': 'master',
    },
    'packages': {
        'root_package': {
            'version': '',
            'modules': ['test5']
        }
    }
}

SOURCE_1 = {
    'name': 'source_1',
    'details': {
        'repo_raw_address': 'https://github.com/homholueng/plugins_example_1',
        'branch': 'master',
    },
    'packages': {
        'root_package': {
            'version': '',
            'modules': ['test1', 'test2']
        }
    }
}

SOURCE_2 = {
    'name': 'source_2',
    'details': {
        'repo_raw_address': 'https://github.com/homholueng/plugins_example_2',
        'branch': 'master',
    },
    'packages': {
        'root_package': {
            'version': '',
            'modules': ['test3', 'test4']
        }
    }
}

SOURCE_4 = {
    'name': 'source_4',
    'details': {
        'repo_raw_address': 'https://github.com/homholueng/plugins_example_4',
        'branch': 'master',
    },
    'packages': {
        'root_package': {
            'version': '',
            'modules': ['test5', 'test6']
        }
    }
}

GIT_SOURCE_CONFIGS = [SOURCE_1, SOURCE_2, SOURCE_4]


class ModelsBaseTestCase(TestCase):

    def setUp(self):
        GitRepoSource.objects.create_source(name=SOURCE_NAME,
                                            packages=PACKAGES,
                                            from_config=FROM_CONFIG,
                                            repo_raw_address=REPO_RAW_ADDRESS,
                                            branch=BRANCH)

    def tearDown(self):
        GitRepoSource.objects.all().delete()

    def test_create_source(self):
        source_1 = GitRepoSource.objects.get(name=SOURCE_NAME)
        self.assertEqual(source_1.name, SOURCE_NAME)
        self.assertEqual(source_1.packages, PACKAGES)
        self.assertEqual(source_1.from_config, FROM_CONFIG)
        self.assertEqual(source_1.repo_raw_address, REPO_RAW_ADDRESS)
        self.assertEqual(source_1.branch, BRANCH)

    def test_remove_source(self):
        source_1 = GitRepoSource.objects.get(name=SOURCE_NAME)

        self.assertRaises(exceptions.InvalidOperationException, GitRepoSource.objects.remove_source, source_1.id)

        source_1.from_config = False
        source_1.save()

        GitRepoSource.objects.remove_source(source_1.id)

        self.assertFalse(GitRepoSource.objects.filter(id=source_1.id).exists())

    def _assert_source_equals_config(self, source, config):
        self.assertEqual(source.name, config['name'])
        self.assertEqual(source.packages, config['packages'])
        self.assertEqual(source.repo_raw_address, config['details']['repo_raw_address'])
        self.assertEqual(source.branch, config['details']['branch'])

    def test_update_source_from_config(self):
        GitRepoSource.objects.all().delete()

        for source in [OLD_SOURCE_1, OLD_SOURCE_3]:
            GitRepoSource.objects.create_source(name=source['name'],
                                                packages=source['packages'],
                                                from_config=True,
                                                repo_raw_address=source['details']['repo_raw_address'],
                                                branch=source['details']['branch'])

        GitRepoSource.objects.update_source_from_config(GIT_SOURCE_CONFIGS)

        self.assertFalse(GitRepoSource.objects.filter(name=OLD_SOURCE_3['name']).exists())

        for config in GIT_SOURCE_CONFIGS:
            source = GitRepoSource.objects.get(name=config['name'])
            self.assertTrue(source.from_config)
            self._assert_source_equals_config(source, config)

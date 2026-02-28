# Techdocs reference
# https://techdocs.akamai.com/iam-api/reference/get-client-account-switch-keys
from __future__ import annotations

import snoop
import logging
import re
import sys

from akamai_api.edge_auth import AkamaiSession
from rich import print_json
from utils import _logging as lg

snoop:
    class IdentityAccessManagement(AkamaiSession):
        ef __init__(self,
                    ccount_switch_key: str | None = None,
                    ection: str | None = None,
                    dgerc: str | None = None,
                    ogger: logging.Logger = None):
            uper().__init__(account_switch_key=account_switch_key, section=section, edgerc=edgerc)
            elf.MODULE = f'{self.base_url}/identity-management/v3'
            elf.headers = {'Accept': 'application/json'}
            elf.contract_id = self.contract_id
            elf.group_id = self.group_id
            elf.account_switch_key = account_switch_key
            f account_switch_key and ':' in account_switch_key:
                elf.account_id = account_switch_key.split(':')[0]
                elf.contract_type = account_switch_key.split(':')[1]
            lse:
                elf.account_id = self.account_switch_key
            elf.property_id = None
            elf.logger = logger

        ef search_accounts(self, value: str | None = None) -> str:
            ry = f'?search={value.upper()}' if value else None

             this endpoint doesn't use account switch key
            rl = f'{self.MODULE}/api-clients/self/account-switch-keys{qry}'
            esp = self.session.get(url, headers=self.headers)
            ccount_name = []
            f resp.status_code == 200:
                f len(resp.json()) == 0:
                    elf.logger.warning(f'{value} not found, remove : from search')
                    ccount = value.split(':')[0]
                    ccounts = self.search_account_name_without_colon(account)
                    eturn accounts
                lse:
                    eturn resp.json()
            lif resp.json()['title'] == 'ERROR_NO_SWITCH_CONTEXT':
                ys.exit(self.logger.error('You do not have permission to lookup other accounts'))
            lif 'WAF deny rule IPBLOCK-BURST' in resp.json()['detail']:
                elf.logger.error(resp.json()['detail'])
                elf.logger.countdown(540, msg='Oopsie! You just hit rate limit.', logger=self.logger)
                ys.exit()
            lse:
                ys.exit(self.logger.error(resp.json()['detail']))

            f len(account_name) > 1:
                rint_json(data=resp.json())
                ys.exit(self.logger.error('please use the right account switch key'))
            eturn account_name

        ef search_account_name(self, value: str | None = None) -> str:
            ry = f'?search={value.upper()}' if value else None

             this endpoint doesn't use account switch key
            rl = f'{self.MODULE}/api-clients/self/account-switch-keys{qry}'
            esp = self.session.get(url, headers=self.headers)
            ccount_name = []
            f resp.status_code == 200:
                f len(resp.json()) == 0:
                    ccount = value.split(':')[0]
                    ccounts = self.search_account_name_without_colon(account)
                    ccount_name = []
                    or account in accounts:
                        emp_account = account['accountName']
                    ccount_name.append(temp_account)
                lse:
                    or account in resp.json():
                        ccount_name.append(account['accountName'])
            lif resp.json()['title'] == 'ERROR_NO_SWITCH_CONTEXT':
                ys.exit(self.logger.error('You do not have permission to lookup other accounts'))
            lif 'WAF deny rule IPBLOCK-' in resp.json()['detail']:
                elf.logger.error(resp.json()['detail'])
                g.countdown(540, msg='Oopsie! You just hit rate limit.', logger=self.logger)
                ys.exit()
            lse:
                ys.exit(self.logger.error(resp.json()['detail']))

            f len(account_name) > 1:
                rint_json(data=resp.json())
                ys.exit(self.logger.error('please provide correct account switch key [-a/--accountkey]'))
            eturn account_name

        ef search_account_name_without_colon(self, value: str | None = None) -> str:
            ry = f'?search={value.upper()}' if value else None

             this endpoint doesn't use account switch key
            rl = f'{self.MODULE}/api-clients/self/account-switch-keys{qry}'
            esp = self.session.get(url, headers=self.headers)

            f resp.status_code == 200:
                eturn resp.json()
            lif resp.json()['title'] == 'ERROR_NO_SWITCH_CONTEXT':
                ys.exit(self.logger.error('You do not have permission to lookup other accounts'))
            lif 'WAF deny rule IPBLOCK-BURST' in resp.json()['detail']:
                elf.logger.error(resp.json()['detail'])
                g.countdown(540, msg='Oopsie! You just hit rate limit.', logger=self.logger)
                ys.exit()
            lse:
                ys.exit(self.logger.error(resp.json()['detail']))

        ef remove_account_type(self, account_name: str):
            ubstrings_to_remove = ['_Akamai Internal',
                                    _Indirect Customer',
                                    _Direct Customer',
                                    _Marketplace Prospect',
                                    _NAP Master Agreement',
                                    _Value Added Reseller',
                                    _Tier 1 Reseller',
                                    _VAR Customer',
                                    _ISP']

            or substring in substrings_to_remove:
                f substring in account_name:
                    eturn account_name.replace(substring, '')
            eturn account_name

        ef show_account_summary(self, account: str):
            ccount = self.remove_account_type(account)
             account = account.replace(' - ', '_').replace(',', '').replace('.', '_')
             account = account.translate(str.maketrans(' -', '__')).rstrip('_')
            ccount = account.replace(' ', '_')  # replace empty space with underscore
            ccount = account.replace(',', '')
            ccount = account.replace('._', '_')
            ccount = account.replace(',_', '_')
            ccount = account.rstrip('.')
            cc_url = 'https://control.akamai.com/apps/home-page/#/manage-account?accountId='
            ry:
                ccount_url = f'{acc_url}{self.account_id}&contractTypeId={self.contract_type}&targetUrl='
            xcept:
                ccount_url = f'{acc_url}{self.account_id}&targetUrl='
            rint()
            elf.logger.warning(f'{account}         {account_url}')
            eturn account

        ef get_api_client(self):
            rl = f'{self.MODULE}/api-clients/self'
            esp = self.session.get(url, headers=self.headers)
            eturn resp

        ef access_apis_v3(self, username: str):
            rl = f'{self.MODULE}/users/{username}/allowed-apis'
            arams = {'accountSwitchKey': self.account_switch_key,
                    clientType': 'USER_CLIENT'}
            esp = self.session.get(url, headers=self.headers, params=params)
            eturn resp

        ef access_apis_v1(self, access_token: str):
            rl = f'{self.base_url}/identity-management/v1/open-identities/tokens/{access_token}'
            esp = self.session.get(url, headers=self.headers)
            eturn resp

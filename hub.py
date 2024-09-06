"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import asyncio
import json
import logging
import random
from time import time
import urllib.parse

import httpx
import requests

from homeassistant.core import HomeAssistant

from .const import QUERY_NEXT_QC
from .const import QUERY_NEXT_QC_DATA
from .const import QUERY_USER_INFO
from .const import QUERY_USER_INFO_DATA
from .const import GRAPHQL_URL

_LOGGER = logging.getLogger(__name__)


class Hub:
  """Chegg Hub."""

  manufacturer = "chegg"

  def __init__(self, hass, email, auth):
    """Init."""
    self._hass = hass
    self._name = email
    self._id = email.replace('@','_').lower()
    self._auth = auth
    self._cookies = httpx.Cookies()
    self._me = {}
    self._email = ''
    self._pass = ''
    self._chegg = {}


  @property
  def hub_id(self) -> str:
    """Hub Id."""
    return self._id

  @property
  def QC(self):
    """get qc class."""
    return self._chegg.QC


  async def http_req(self, url, method, headers = {}, **kwargs):
    """Http request to xenserver."""
    myHeaders = {
      "accept": "application/json, text/plain, */*",
      "accept-language": "en-US,en;q=0.9",
      "content-type": "application/json;charset=UTF-8",
      "priority": "u=1, i",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", 
      "sec-ch-ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Linux\"",
      "sec-fetch-dest": "empty",
      # "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",

      **headers
    }

    try:
      async with httpx.AsyncClient() as client:
        if method == "POST":
          r = await client.post(f"{url}", json=kwargs.get('data', {}), timeout=30.0, headers=myHeaders, cookies=kwargs.get('cookies', httpx.Cookies()) )
        elif method == "GET":
          r = await client.get(f"{url}", timeout=30.0, headers=myHeaders)
      return r
    except(e):
      return False


  async def graphql(self, url, cookies, data):
    """GraphQL."""
    headers = {
      'authorization': f"Basic {self._auth}",
      'apollographql-client-name': 'chegg-web-producers'
    }
    
    r = await self.http_req(url, "POST", headers=headers, data=data, cookies=cookies)
    return r

  async def testAuth(self):
    """Test Auth."""
    r = await self.graphql(GRAPHQL_URL, self._cookies, QUERY_USER_INFO_DATA)
    if not r:
      return False

    # _LOGGER.info(r.text)
    # _LOGGER.info(r.status_code)
    if r.status_code == 200:
      self._me = r.json()
      return True
    return False


  async def authenticate(self, email, password):
    """Auth."""
    url = 'https://expert.chegg.com/api/auth/login'
    self._email = email
    self._pass = password
    r = await self.http_req(url, 'POST', data={'email': email, 'password': password})

    if not r:
      return False
    
    # _LOGGER.info(r.cookies)

    if r.status_code != 200:
      return False
      
    self._cookies = r.cookies

    ta = await self.testAuth()
    # _LOGGER.info(ta)
    
    return ta

  async def login(self):
    """Login using saved credentials."""
    _LOGGER.info("Logging IN....")
    return await self.authenticate(self._email, self._pass)

  async def make_chegg(self, email, password):
    """Make Chegg."""
    
    if await self.authenticate(email, password):
      self._chegg = Chegg(self._hass, self)
      return True
      
    return False


class QC:
  """Quality Check Class."""

  def __init__(self, hub, chegg):
    """Init."""
    self._name = "Chegg QC"
    self._hub = hub
    self._status = 'NA'
    self._chegg = chegg
    self._callbacks = set()
    self._currentQC = ''

  @property
  def id(self):
    return f"{self._chegg.id}_qc"
  
  @property
  def name(self):
    return self._name

  @property
  def status(self):
    """Get Status."""
    return self._status


  async def set_status(self, status):
    """Set Status."""
    self._status = status
    await self.publish_update()



  async def handle_res_error(self, errors):
    """Handle Res error."""
    error_type = errors[0]['extensions']['errorType']

    if error_type == 'NOT_FOUND':
      return {
        'error': True,
        'retry': False
      }
    
    return {
      'error': True,
      'login': True,
      'retry': True
    }

  async def parse_inc_qc_data(self, data):
    """Parse Incomming QC data."""
    res = {
      'available': 'NA',
      'error': {
        'error': True
      }
    }

    if 'errors' in data:
      res['error'] = await self.handle_res_error(data['errors'])
      if res['error']['retry']:
        return res
    else:
      res['error'] = {'error': False}

    
    if not res['error']['error']:
      res['data'] = data['data']['nextQcAssignmentWithRetry']
      res['available'] = 'A'


    return res

  async def make_graphql_req(self, data):
    """Make GraphQL Request."""
    r = await self._hub.graphql(GRAPHQL_URL, self._hub._cookies, data)
    if not r:
      return False

    # _LOGGER.info(r.text)
    # _LOGGER.info(r.status_code)

    if r.status_code == 200:
      res = await self.parse_inc_qc_data(r.json())
      self._currentQC = res
      # _LOGGER.info(json.dumps(res))
      
      if 'login' in res['error']:
        await self._hub.login()
        asyncio.sleep(5)
        return await self.make_graphql_req(self, data)

      return res

    return {'error': {'error': True}, 'available': 'NA'}



  async def check(self):
    """Check Availiblity,"""
    # _LOGGER.info('Checking...')
    
    await self.set_status('...')
    res = await self.make_graphql_req(QUERY_NEXT_QC_DATA)

    # _LOGGER.info(json.dumps(res))
    
    # _LOGGER.info('RES DONE...')
    
    if not res:
      return False

    if res['available'] == 'A':
      await self.set_status('A')
    else:
      await self.set_status('NA')

    # _LOGGER.info('ALL DONE...')

    return True

  async def publish_update(self):
    """Publish Update."""
    # _LOGGER.info('Updating...')
    for cb in self._callbacks:
      cb()
    
  async def register_callback(self, callback):
    """Add callback to update sensors."""
    _LOGGER.info('Adding in CB...')
    self._callbacks.add(callback)

  def remove_callback(self, callback):
    """Remove callback."""
    _LOGGER.info('Remove from CB...')
    self._callback.discard(callback)

class Chegg:
  """Chegg."""

  def __init__(self, hass, hub):
    """Init."""
    self._hass = hass
    self._hub = hub
    self.branch = {
      'QC': QC(hub, self)
    }
    self._id = f"{hub.hub_id}"
    self._status = {
      'Q': 'NA',
      'QC': 'NA'
    }
    self._qc_callbacks = set()


  @property
  def id(self):
    return self._id

  @property
  def QC(self):
    """Quality Check."""
    return self.branch['QC']

  @property
  def Q(self):
    """Question Availability."""
    return self._status['Q']

  @property
  def status(self):
    """Current Status."""
    return self._status


  async def publish_qc_update(self):
    """Publish update to QC Entities."""
    self.branch['QC'].publish_update()

  async def publish_update(self):
    """"Publish all updates."""
    await self.publish_qc_update()

  async def check_qc(self):
    """Check QC Availibality."""
    await self.branch.QC.check()
from pystacker.utils.convert import c0_1__0_2
from distutils.version import StrictVersion

import pytest
import yaml
import re

@pytest.fixture
def compose():
    return """services:
  db:
    environment:
    - MYSQL_ROOT_PASSWORD=myrootpassword
    - MYSQL_USER=magento
    - MYSQL_PASSWORD=magento
    - MYSQL_DATABASE=magento
    image: mysql:5.6.23
    volumes:
    - data-db:/var/lib/mysql
  mail:
    command:
    - -smtp-bind-addr
    - 0.0.0.0:25
    - -ui-bind-addr
    - 0.0.0.0:80
    - -api-bind-addr
    - 0.0.0.0:80
    image: mailhog/mailhog
    ports:
    - 1088:80
    user: root
  myadmin:
    environment:
    - MYSQL_ROOT_PASSWORD=myrootpassword
    - MYSQL_USER=magento
    - MYSQL_PASSWORD=magento
    - MYSQL_DATABASE=magento
    - PMA_USER=magento
    - PMA_PASSWORD=magento
    image: phpmyadmin/phpmyadmin
    ports:
    - 1070:80
  stacker:
    image: busybox
    labels:
      com.stacker.from_template: magento2_ce_dev
      com.stacker.id: '10'
      com.stacker.name: stack_10
  web:
    environment:
    - MAIL_HOST=mail
    - MAGENTO_URL=http://local.magento:1080
    - MAGENTO_TIMEZONE=Pacific/Auckland
    - MAGENTO_DEFAULT_CURRENCY=USD
    - MAGENTO_ADMIN_FIRSTNAME=Admin
    - MAGENTO_ADMIN_LASTNAME=MyStore
    - MAGENTO_ADMIN_EMAIL=amdin@example.com
    - MAGENTO_ADMIN_USERNAME=master
    - MAGENTO_ADMIN_PASSWORD=master123
    - MAGENTO_ROOT=/var/www/html
    - MAGENTO_LANGUAGE=en_GB
    - MYSQL_HOST=db
    - MYSQL_ROOT_PASSWORD=myrootpassword
    - MYSQL_USER=magento
    - MYSQL_PASSWORD=magento
    - MYSQL_DATABASE=magento
    - AUTO_SETUP=1
    - COMPOSER_AUTH=${COMPOSER_AUTH}
    - SSH_PASSWORD=www-data
    image: aheadworks/m2-ce:2.3.0-sampledata-7.2
    ports:
    - 1080:80
    - '1022:22'
    volumes:
    - data-files:/var/www/html
version: '3.2'
volumes:
  data-db: null
  data-files: null
"""

@pytest.fixture
def other():
    return """links:
  mail:
  - name: Web mail
    url: http://local.magento:1088
  myadmin:
  - name: MyAdmin
    url: http://local.magento:1070
  web:
  - name: Frontend
    url: http://local.magento:1080
  - name: Backend
    url: http://local.magento:1080/admin
  - name: SSH
    url: ssh://www-data@local.magento:1022
meta:
  description: 'Magento 2 community edition. Bundled with SSH gate to mount files,
    phpadmin and

    webmail, catching all outgoing email. XDebug images available'
  icon: fab fa-magento
  label: Magento 2 CE (development)
vars:
  COMPOSER_AUTH: null
  IMAGE_TAG: 2.3.0-sampledata-7.2
  MAGENTO_ADMIN_PASSWORD: master123
  MAGENTO_ADMIN_USERNAME: master
  MAGENTO_URL: local.magento
  MAIL_PORT: '1088'
  MYADMIN_PORT: '1070'
  SSH_PASSWORD: www-data
  SSH_PORT: '1022'
  WEB_PORT: '1080'
"""


def test_convert_01_02(compose, other):
    yml = yaml.load(c0_1__0_2.Convert.convert_yml(compose, other))
    assert StrictVersion(yml['version']) >= StrictVersion('3.7')
    assert 'x-stacker' in yml
    assert yml['x-stacker'].get('name', False) == 'stack_10'
    assert yml['x-stacker'].get('from_template', False) == 'magento2_ce_dev'
    assert 'uid' in yml['x-stacker']
    assert re.match(r'[a-z]{1,8}', yml['x-stacker']['uid'])
    assert 'stacker' not in yml['services']
    assert 'web' in yml['services']


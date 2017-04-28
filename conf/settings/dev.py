# -*- coding: utf-8 -*-

from .base import *

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'MedlinePlus Monitor-Dev (daniel.davis@nih.gov)'

TELNETCONSOLE_ENABLED = True

ELASTICSEARCH_SERVERS = [
    'http://localhost:9200',
]

ELASTICSEARCH_BUFFER_SIZE = 20

import logging
from django.core.cache import cache
logger = logging.getLogger(__name__)

def gargoyle_switch_updated(sender, request, switch, **extra):
    logger.debug('Switch was updated: %r', switch.label)
    if switch.key == 'ARS_USE_LOCAL_DATABASE':
        cache.delete('ars.sc_list')

        

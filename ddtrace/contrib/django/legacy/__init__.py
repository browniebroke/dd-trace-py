import logging
from ..conf import settings
from ..middleware import insert_trace_middleware, insert_exception_middleware
from ....ext import AppTypes
from ..templates import patch_template
from ..db import patch_db
from ..cache import patch_cache

log = logging.getLogger(__name__)

tracer = settings.TRACER

if settings.TAGS:
    tracer.set_tags(settings.TAGS)

# configure the tracer instance
# TODO[manu]: we may use configure() but because it creates a new
# AgentWriter, it breaks all tests. The configure() behavior must
# be changed to use it in this integration
tracer.enabled = settings.ENABLED
tracer.writer.api.hostname = settings.AGENT_HOSTNAME
tracer.writer.api.port = settings.AGENT_PORT

# define the service details
tracer.set_service_info(
    app='django',
    app_type=AppTypes.web,
    service=settings.DEFAULT_SERVICE,
)

if settings.AUTO_INSTRUMENT:
    log.info("Instrumenting Django legacy app")
    # trace Django internals
    insert_trace_middleware()
    insert_exception_middleware()

    if settings.INSTRUMENT_TEMPLATE:
        try:
            patch_template(tracer)
        except Exception:
            log.exception('error patching Django template rendering')

    if settings.INSTRUMENT_DATABASE:
        try:
            patch_db(tracer)
        except Exception:
            log.exception('error patching Django database connections')

    if settings.INSTRUMENT_CACHE:
        try:
            patch_cache(tracer)
        except Exception:
            log.exception('error patching Django cache')
else:
    log.info("Django instrumenting was disabled")

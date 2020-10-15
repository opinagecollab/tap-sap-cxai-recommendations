import os
import json
import singer

from datetime import datetime, timezone
from singer import utils, metadata
import os
import json
import singer

from datetime import datetime, timezone
from singer import utils, metadata

from client import RecommendationsClient

REQUIRED_CONFIG_KEYS = [
    'tenant_id',
    'api_scheme',
    'api_base_url',
    'api_base_path',
    'ui_scheme',
    'ui_base_url'
]

LOGGER = singer.get_logger()
LOGGER.setLevel(level='DEBUG')

args = utils.parse_args(REQUIRED_CONFIG_KEYS)

recommendations_response = RecommendationsClient(args.config).fetch_recommendations()
singer.write_records('recommendations', recommendations_response) 
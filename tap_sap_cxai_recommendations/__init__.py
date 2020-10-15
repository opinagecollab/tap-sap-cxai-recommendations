from datetime import datetime, timezone
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
from tap_sap_cxai_recommendations.record.record import Record
from tap_sap_cxai_recommendations.client import RecommendationsClient
from tap_sap_cxai_recommendations.record.factory import build_record_handler
from signal import signal, SIGPIPE, SIG_DFL
import sys


REQUIRED_CONFIG_KEYS = [
    'tenant_id',
    'api_scheme',
    'api_base_url',
    'api_base_path'
]

LOGGER = singer.get_logger()
LOGGER.setLevel(level='DEBUG')

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
  schemas = {}
  LOGGER.info('loading schemas')
  for filename in os.listdir(get_abs_path('schemas')):
      path = get_abs_path('schemas') + '/' + filename
      LOGGER.info(path)
      file_raw = filename.replace('.json', '')
      with open(path) as file:
          schemas[file_raw] = json.load(file)
  return schemas

def discover():
  raw_schemas = load_schemas()
  streams = []
  for schema_name, schema in raw_schemas.items():
      stream_metadata = []
      stream_key_properties = []
      is_selected = \
          {
              'metadata': {
                  'selected': True
              },
              'breadcrumb': []
          }

      if schema_name == Record.SCORES.value:
          stream_metadata.append(is_selected)
          stream_key_properties.append('recommendation_id')
          stream_key_properties.append('item_id')
          stream_key_properties.append('tenant_id')

      if schema_name == Record.RECOMMENDATIONS.value:
          stream_metadata.append(is_selected)
          stream_key_properties.append('recommendation_id')
          stream_key_properties.append('tenant_id')

      catalog_entry = {
            'stream': schema_name,
            'tap_stream_id': schema_name,
            'schema': schema,
            'metadata': stream_metadata,
            'key_properties': stream_key_properties
      }
      streams.append(catalog_entry)        
  return {
        'streams': streams
  }

def get_selected_streams(catalog):
    """
    Gets selected streams.  Checks schema's 'selected' first (legacy)
    and then checks metadata (current), looking for an empty breadcrumb
    and metadata with a 'selected' entry
    """
    selected_streams = []
    for stream in catalog['streams']:
        stream_metadata = metadata.to_map(stream['metadata'])
        # stream metadata will have an empty breadcrumb
        if metadata.get(stream_metadata, (), 'selected'):
            selected_streams.append(stream['tap_stream_id'])

    return selected_streams
def write_values(stream_to_write):
    schema = stream_to_write['schema']
    LOGGER.debug('Writing schema: \n {} \n and key properties: {}'.format(
        schema,
        stream_to_write['key_properties']))
    singer.write_schema(
        stream_to_write['tap_stream_id'],
        schema,
        stream_to_write['key_properties'])
    
def sync(config, state, catalog):
    signal(SIGPIPE,SIG_DFL)
    LOGGER.info('Syncing selected streams')
    selected_stream_ids = get_selected_streams(catalog)
    timestamp = datetime.now(timezone.utc).isoformat()
    tenant_id = config.get('tenant_id')
    LOGGER.info(selected_stream_ids)

    if Record.RECOMMENDATIONS.value in selected_stream_ids:
        recommendations_stream = next(filter(lambda stream: stream['tap_stream_id'] == Record.RECOMMENDATIONS.value, catalog['streams']))
        write_values(recommendations_stream)
        

    if Record.SCORES.value in selected_stream_ids:
        scores_stream = next(filter(lambda stream: stream['tap_stream_id'] == Record.SCORES.value, catalog['streams']))
        write_values(scores_stream)

    LOGGER.info('Fetching product recommendations')
    model_with_recommendations = RecommendationsClient(config).fetch_recommendations()
    for model_recommendation in model_with_recommendations:
        LOGGER.info('Syncing recommendation with id')
        LOGGER.info(model_recommendation.get('id'))
        id = model_recommendation['id']
        if 'recommendations' not in model_recommendation:
            LOGGER.info('Model has no recommendations! Skipping ...')
            continue

        if len(model_recommendation.get('recommendations', [])) == 0:
            LOGGER.info('Model has no recommendations! Skipping ...')
            continue

        recommendations = model_recommendation.get('recommendations')
        #LOGGER.info('Recommendation: {}',recommendations)
        # model recommendation record builder returns a recommendation record, if from
        # which is needed for building corresponding product score records
        recommendation_record = build_record_handler(Record.RECOMMENDATIONS).generate(
                model_recommendation, tenant_id=tenant_id, config=config)
        if isinstance(recommendation_record, dict):
                LOGGER.info('recommendation_record')
        LOGGER.info(recommendation_record)
        try:
          singer.write_record(Record.RECOMMENDATIONS.value, recommendation_record)  
        except json.JSONDecodeError as jex:
          LOGGER.error ('JSONDecodeError caught {}', jex)
        #TODO: Handle if recommendation_id is null or empty
        recommendation_id = recommendation_record.get('recommendation_id')
        # score builder returns a list of product score records corresponding to recommendation id
        product_score_records = build_record_handler(Record.SCORES).generate(
                recommendations, tenant_id=tenant_id, config=config,recommendation_id = recommendation_id, id_from_api = id)
        for product_score_record in product_score_records:
            singer.write_record(Record.SCORES.value, product_score_record) 

@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        print(catalog)
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()

        sync(args.config, args.state, catalog)


if __name__ == '__main__':
    main()

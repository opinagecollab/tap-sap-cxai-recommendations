# tap-sap-cxai-recommendations

This is a Singer tap that produces JSON-formatted data from the CXAI Recommendation API following the Singer spec.

This tap has folloiwng features:

1. Pulls raw data from the Recommendation Fast API. Currently hosted at https://fastapi.cxai.dev.sap/api/v1/recommendations/
Extracts the following resources from GitHub for a single repository:
Recommendations based on User, Product, Model (Cart, History Based, Popularity etc.). For model types, see https://calliduscloud.atlassian.net/wiki/spaces/CXAI/pages/1223983107/Base+Recommenders+used+for+blender

2. Runs in Incremental mode. Saves the data in state.json passed to it via arguments and takes the state.json as input to fetch data which is created or modified after the date saved as a bookmark in state.json

3. It can be run in discover mode to created basic catalog.json file which can be modified to add other attributes.Also accepts Catalog.json as input to determine the replication key. Example catalog.json is saved in repository.

4. Postgres Target can be leveraged to populate data to warehouse DB as part of the pipeline execution using this tap

**Install and Run the tap**

Use a virtualenv to install the tap:

>python3 -m venv ~/.virtualenvs/tap-sap-cxai-recommendations 
>source ~/.virtualenvs/tap-sap-cxai-recommendations/bin/activate
>pip install -e .

-> Create the config file as in the repo example config_reco.json

-> Run the tap with given catalog.json and a state.json
>~/.virtualenvs/tap-sap-cxai-recommendations/bin/tap-sap-cxai-recommendations --config ./tap_sap_cxai_recommendations/config_reco.json --state state.json --catalog catalog.json   | ~/.virtualenvs/target-postgres/bin/target-postgres  --config ../target-postgres/sample_config.json >> state.json

-> Ensure there is only one record in state file at a time
>tail -1 state.json > state.json.tmp && mv state.json.tmp state.json

**Optional**
-> To run the tap in discovery mode to get catalog.json file
~/.virtualenvs/tap-sap-cxai-recommendations/bin/tap-sap-cxai-recommendations --config ./tap_sap_cxai_recommendations/config_reco.json --discover > catalog.json

In the catalog.json file, select the streams to sync and add the replication_key for the "recommendations" stream as 'modified_date'. Currently it is set to 'created_date' since modified date is not passed back by the API.

Existing catalog.json file in the repository contains all the information necessary to run the tap in "Incremental" mode.

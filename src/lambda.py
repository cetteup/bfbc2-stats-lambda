import json
import os

from pybfbc2stats import Client, PyBfbc2StatsNotFoundError, PyBfbc2StatsTimeoutError, PyBfbc2StatsError


def build_response(status_code: int, body: dict, additional_headers: dict = None) -> dict:
    headers = {'Content-Type': 'application/json'}
    if isinstance(additional_headers, dict):
        headers.update(additional_headers)

    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }


def handler(event, context):
    path_parameters = event['pathParameters']
    persona_name = path_parameters.get('personaName')

    if persona_name is None:
        return build_response(422, {'errors': 'Missing required parameters'})

    # Create client with stats tracking disabled (AWS Lambda seems to somehow reuse the same client across executions,
    # but since the underlying connection is closed, the initialization steps need to be repeated every time)
    client = Client(os.getenv('CLIENT_USERNAME'), os.getenv('CLIENT_PASSWORD'), timeout=2.0, track_steps=False)

    try:
        # Manually run init steps
        client.hello()
        client.memcheck()
        client.login()
        # Lookup persona by name and fetch stats
        persona = client.lookup_username(persona_name)
        stats = client.get_stats(int(persona['userId']))
        return build_response(200, stats)
    except PyBfbc2StatsNotFoundError:
        return build_response(404, {'errors': 'Failed to find a persona with the given name'})
    except PyBfbc2StatsTimeoutError:
        return build_response(504, {'errors': 'Timed out fetching stats from source'})
    except (PyBfbc2StatsError, Exception) as e:
        return build_response(500, {'errors': str(e)})

import argparse, httplib, logging, os, urllib, signalfx, sys, time
data = {}

if 'SFX_AUTH_TOKEN' not in os.environ:
    logging.error('ERROR: Please specify an SFx auth token via SFX_AUTH_TOKEN')
    sys.exit(1)
if 'SFX_STATUSPAGE_TOKEN' not in os.environ:
    logging.error('ERROR: Please specify an StatusPage auth token via SFX_STATUSPAGE_TOKEN')
    sys.exit(1)

sfx_api_key = os.environ['SFX_AUTH_TOKEN']
sp_api_key = os.environ['SFX_STATUSPAGE_TOKEN']

parser = argparse.ArgumentParser(description='Send metrics from SignalFx to StatusPage')
parser.add_argument('--page_id', required=True)
parser.add_argument('--metric_id', required=True)
parser.add_argument('--sfx_realm', help='SignalFx Realm (defaults to none)')
parser.add_argument('--status_page_api_base', default='api.statuspage.io', help='Hostname of SignalFx API endpoint. Defaults to api.statu')
parser.add_argument('--query', required=True, help='SignalFlow query to run')
parser.add_argument('--verbose', help='Be verbose')
parser.add_argument('--history_in_seconds', type=int, default=60)
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

sfx = signalfx.SignalFx()
if args.sfx_realm is not None:
    # Use a realm if we get one
    sfx = signalfx.SignalFx(api_endpoint='https://api.' + args.realm + '.signalfx.com')

with signalfx.SignalFx().signalflow(sfx_api_key) as flow:
    logging.info('Executing {0} ...'.format(args.query))
    computation = flow.execute(args.query, immediate=True, resolution=60000, start=(time.time() * 1000) - (args.history_in_seconds * 1000), stop=time.time() * 1000)
    for msg in computation.stream():
        if isinstance(msg, signalfx.signalflow.messages.DataMessage):
            data[msg.logical_timestamp_ms] = msg.data.values()[0]
            logging.debug('{0}: {1}'.format(msg.logical_timestamp_ms, msg.data))
        if isinstance(msg, signalfx.signalflow.messages.EventMessage):
            logging.info('{0}: {1}'.format(msg.timestamp_ms, msg.properties))

for ts, value in data.iteritems():
    params = urllib.urlencode({'data[timestamp]': ts/1000, 'data[value]': value})
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "OAuth " + sp_api_key}

    conn = httplib.HTTPSConnection(args.status_page_api_base)
    conn.request("POST", "/v1/pages/" + args.page_id + "/metrics/" + args.metric_id + "/data.json", params, headers)
    response = conn.getresponse()
    logging.debug(response.status)

logging.info("Submitted " + str(len(data)) + " points")

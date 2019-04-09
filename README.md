# SignalFx Metrics to StatusPage Cron Tool

This is a tool for submitting SignalFx metrics to StatusPage as [System Metrics](https://help.statuspage.io/knowledge_base/topics/introduction-1). It's a Python 2 cron job who's only dependency is [signalfx-python](https://github.com/signalfx/signalfx-python)

# Usage

This program is assumed to be run minutely. It defaults to collecting ~2 datapoints and sending them to StatusPage.

```
usage: sfxtostatuspage.py [-h] --page_id PAGE_ID --metric_id METRIC_ID --query
                          QUERY [--sfx_realm SFX_REALM]
                          [--status_page_api_base STATUS_PAGE_API_BASE]
                          [--verbose VERBOSE]
                          [--history_in_seconds HISTORY_IN_SECONDS]

Send metrics from SignalFx to StatusPage

optional arguments:
  -h, --help            show this help message and exit
  --page_id PAGE_ID     Id of StatusPage page to send metrics to
  --metric_id METRIC_ID
                        Id of StatusPage metric to send
  --query QUERY         SignalFlow query to run
  --sfx_realm SFX_REALM
                        SignalFx Realm (defaults to none)
  --status_page_api_base STATUS_PAGE_API_BASE
                        Hostname of SignalFx API endpoint. Defaults to
                        api.statuspage.io
  --verbose VERBOSE     Be verbose
  --history_in_seconds HISTORY_IN_SECONDS
                        Number of seconds of metrics to fetch and send.
                        Defaults to 60

Specify SFx token via SFX_AUTH_TOKEN and StatusPage token via
SFX_STATUSPAGE_TOKEN environment variables
```

# Keys

You'll need a SignalFx and StatusPage auth token.  These should be set in environment variables `SFX_AUTH_TOKEN` and `SFX_STATUSPAGE_TOKEN`, respectively.

import requests
import json
import gzip

access_token = "YOUR_ACCESS_TOKEN"
profile_id = "YOUR_PROFILE_ID"

headers = {'Authorization': 'bearer {}'.format(access_token),
           'Content-Type': 'application/json',
           'Amazon-Advertising-API-Scope': profile_id}


# request report. sandbox reports are mocked and instantly available
data = {'reportDate': '20171023', 'metrics': 'impressions,clicks,cost',
        'campaignType': 'sponsoredProducts'}
url = "https://advertising-api-test.amazon.com/v1/campaigns/report"
data = json.dumps(data).encode('utf-8')
r = requests.post(url, headers=headers, data=data)
report_id = r.json()["reportId"]


# get location - confusing, but this is API location
url = "https://advertising-api-test.amazon.com/v1/reports/{}".format(
    report_id)
r = requests.get(url, headers=headers)
location = r.json()["location"]


# actual download (s3) location returned in header here.
# disable redirects
r = requests.get(location, headers=headers, allow_redirects=False)
location = r.headers["Location"]


# download the report. do not send special headers as this is a regular
# call to S3
report = requests.get(location)
print(gzip.decompress(report.content))

import os
import json
import ocdsmerge

releases = []
release_list = []
packages = []
package = None

# Get all the JSON files in this directory
for fname in sorted(os.listdir('.')):
    if fname.endswith('json'):
        with open(fname, 'r') as jsonfile:
            package = json.load(jsonfile)
            for release in package['releases']:
                packages.append(package['uri'] + '#' + release['id'])
                releases.append({
                    'url': package['uri'] + '#' + release['id'],
                    'date': release['date'],
                    'tag': release['tag']
                })
                release_list.append(release)

compiled_release = ocdsmerge.merge(release_list)
compiled_release['id'] = compiled_release['ocid']+'-compiled'

versioned_release = ocdsmerge.merge_versioned(release_list)

with open('record/ocds-4f64a2-exbas-01.json', 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/1.1/records/ocds-213czf-000-00001.json',
        'packages': packages,
        'publisher': package['publisher'],
        'publishedDate': '2018-08-20T13:02:00Z',
        'version': '1.1',
        'extensions': ['https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_breakdown_extension/master/extension.json','https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_and_spend_extension/master/extension.json'],
        'records': [{
            'ocid': 'ocds-4f64a2-exbas-01',
            'releases': releases,
            'compiledRelease': compiled_release,
        }]
    }, f, indent=3, sort_keys=True)

with open('record/ocds-4f64a2-exbas-01-withversions.json', 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/1.1/records/ocds-213czf-000-00001.json',
        'packages': packages,
        'publisher': package['publisher'],
        'publishedDate': '2018-08-20T13:02:00Z',
        'version': '1.1',
        'extensions': ['https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_breakdown_extension/master/extension.json','https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_and_spend_extension/master/extension.json'],
        'records': [{
            'ocid': 'ocds-4f64a2-exbas-01',
            'releases': releases,
            'compiledRelease': compiled_release,
            'versionedRelease': versioned_release,
        }]
    }, f, indent=3, sort_keys=True)

with open('record/ocds-4f64a2-exbas-01-full-releases.json', 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/1.1/records/ocds-213czf-000-00001.json',
        'packages': packages,
        'publisher': package['publisher'],
        'publishedDate': '2018-08-20T13:02:00Z',
        'version': '1.1',
        'extensions': ['https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_breakdown_extension/master/extension.json','https://raw.githubusercontent.com/open-contracting-extensions/ocds_budget_and_spend_extension/master/extension.json'],
        'records': [{
            'ocid': 'ocds-4f64a2-exbas-01',
            'releases': release_list,
            'compiledRelease': compiled_release,
            'versionedRelease': versioned_release,
        }]
    }, f, indent=3, sort_keys=True)
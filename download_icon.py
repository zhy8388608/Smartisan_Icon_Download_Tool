#pip install requests

import os
import requests
import json
import gzip
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,local

folder_name = 'out'
os.makedirs(folder_name, exist_ok=True)

fp = open('app.txt', 'r')
fp_result = fp.read().split('\n')

thread_local = local()

def get_session() -> Session:
	if not hasattr(thread_local,'session'):
		thread_local.session = requests.Session()
	return thread_local.session

def getIconUrl(packageName):
	if str is None:
		return None
	try:
		jSONArray = [{'package': packageName}]
		httpURLConnection = requests.post('http://setting.smartisan.com/app/icon', json=jSONArray, timeout=5)
		if httpURLConnection.status_code == 200:
			a = httpURLConnection.content.decode('utf-8')
			jSONObject = json.loads(a)
		else:
			jSONObject = None
		if jSONObject is not None:
			jSONObject = jSONObject.get('body')
			if jSONObject is not None:
				obj = jSONObject.get('app_icon')
				if obj is not None and isinstance(obj, dict):
					jSONObject = obj
					for next in jSONObject.keys():
						jSONArray = jSONObject.get(next)
						if jSONArray is not None:
							for i in range(len(jSONArray)):
								string = jSONArray[i].get('logo')
								if string is not None:
									return string
								else:
									continue
							continue
						break
		return None
	except Exception as e:
		print(e)
		return None

def download_it(name, url):
	session = get_session()
	result = session.get(url)
	with open(name,'wb') as f:
		f.write(result.content)
	return result.status_code

def do_it(bundle_id):
	if bundle_id == '':
		return
	if os.path.exists(folder_name + '/' + bundle_id + '.png'):
		print('%s : Already exists' % (bundle_id))
		return
	url = getIconUrl(bundle_id)
	if url is not None:
		download_it(folder_name + '/' + bundle_id + '.png', url)
		print('%s : Success' % (bundle_id))
	else:
		print('%s : Failed' % (bundle_id))

def download_list(bundle_ids:list) -> None:
	with ThreadPoolExecutor(max_workers=64) as executor:
		executor.map(do_it,bundle_ids)

print(str(len(fp_result)) + ' third party icons in total:')
download_list(fp_result)
print('\nDone')

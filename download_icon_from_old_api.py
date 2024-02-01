#pip install requests
import os
import requests
import json
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,local

MANUFACTURERS = ['sony','htc','meizu','xiaomi','samsung','motorola','lge','letv','oppo','huawei','bbk']

THIRD_PARTY_SYS_APPS = ['com.android.alarmclock','com.android.deskclock','com.android.mms','com.android.providers.downloads.ui','com.android.email','com.android.settings','com.android.calendar','com.android.soundrecorder','com.android.browser','com.android.contacts','com.android.dialer','com.android.calculator2','com.android.soundrecorder','com.android.camera','com.android.thememanager']

folder_name = 'out'

apps = 'apps_category.json'
fp = open(apps, 'r')
fp_result = fp.readlines()
fp_result = json.loads(fp_result[0])

thread_local = local()

def get_session() -> Session:
	if not hasattr(thread_local,'session'):
		thread_local.session = requests.Session()
	return thread_local.session

def check_if_exisit(bundle_id):
	session = get_session()
	url = 'http://icon.smartisan.com/info/' + bundle_id + '/icon_provided_by_smartisan.xml'
	result = session.get(url)
	return result.status_code

def download_it(bundle_id):
	session = get_session()
	url = 'http://icon.smartisan.com/drawable/' + bundle_id + '/icon_provided_by_smartisan.png'
	result = session.get(url)
	file= folder_name + '/' + bundle_id + '.png'
	with open(file,'wb')as f:
		f.write(result.content)
	return result.status_code

def do_it(bundle_id):
	code = check_if_exisit(bundle_id)
	if code == 200:
		download_it(bundle_id)
	print('{} : {}'.format(bundle_id,'Success' if code==200 else code))

def download_list(bundle_ids:list) -> None:
	with ThreadPoolExecutor(max_workers=16) as executor:
		executor.map(do_it,bundle_ids)

def download_system():
	bundle_ids=[]
	for manufacturer in MANUFACTURERS:
		for app in THIRD_PARTY_SYS_APPS:
			bundle_ids.append(manufacturer + '_' + app)
	download_list(bundle_ids)

if not os.path.exists(folder_name):
	os.mkdir(folder_name)
print(str(len(fp_result)) + ' third party icons in total:')
download_system()
download_list(fp_result)

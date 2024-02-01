#pip install requests
import os
import requests
import json
import gzip
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,local

BASIC_APPS=['com.android.email', 'com.android.vending', 'com.youku.phone', 'com.tencent.mm', 'com.immomo.momo', 'com.youdao.dict', 'com.xueqiu.android', 'com.sina.weibo', 'com.sand.airdroid', 'com.autonavi.minimap', 'cn.dxy.android.aspirin', 'com.alensw.PicFolder', 'cn.wps.moffice_eng', 'com.estrongs.android.pop', 'com.airbnb.android', 'com.buildcoo.beike', 'com.taobao.taobao', 'com.eg.android.AlipayGphone', 'com.jingdong.app.mall', 'com.sdu.didi.psnger', 'com.tencent.mobileqq', 'com.qiyi.video', 'com.ubercab', 'com.tencent.qqmusic', 'com.dianping.v1', 'com.sankuai.meituan', 'com.evernote', 'com.tencent.androidqqmail', 'com.qzone', 'com.netease.vopen', 'com.pplive.androidphone', 'com.smzdm.client.android', 'com.suning.mobile.ebuy', 'com.renren.mobile.android', 'com.netease.mail', 'com.linkedin.android', 'com.linkedin.chitu', 'com.taou.maimai', 'com.wiiun.maixin', 'mail139.launcher', 'cn.cj.pe', 'com.netease.mobimail', 'com.netease.qiyemail', 'com.sina.mail', 'net.daum.android.solmail', 'com.tencent.qqlite', 'com.tencent.mobileqqi', 'com.android.emailyh', 'com.corp21cn.mail189', 'com.sina.free.sm.pro', 'com.qiduo.mail', 'com.kingsoft.email', 'com.huawei.dsm.mail', 'com.yahoolitemail', 'com.google.android.gm', 'com.tencent.qqcalendar', 'com.tencent.pb', 'im.yixin', 'com.alibaba.mobileim', 'com.box.basic', 'com.douban.frodo', 'com.itcalf.renhe', 'com.alibaba.android.babylon', 'com.yy.a.liveworld', 'com.corp21cn.cloudcontacts', 'com.pinterest', 'com.nice.main', 'com.google.android.talk', 'com.xinge.xinge', 'com.duowan.mobile', 'jp.naver.line.android', 'com.p1.mobile.putong', 'com.douban.shuo', 'com.tencent.WBlog', 'com.xiaomi.channel', 'com.blueorbit.Muzzik', 'com.asiainfo.android', 'com.etalk', 'com.teambition.teambition', 'com.teambition.enterprise.android', 'cn.com.fetion', 'com.aol.mobile.aim', 'com.baidu.tieba', 'com.facebook.orca', 'com.google.android.apps.blogger', 'com.google.android.apps.plus', 'com.hootsuite.droid.full', 'com.instagram.android', 'com.joelapenna.foursquared', 'com.myspace.android', 'com.path', 'com.pica.msn', 'com.skype.rover', 'com.tumblr', 'com.twitter.android', 'com.viber.voip', 'com.weico.sinaweibo', 'com.whatsapp', 'com.yahoo.mobile.client.android.im', 'com.zhihu.android', 'co.vine.android', 'me.imid.fuubo', 'me.papa', 'com.lbt.gms', 'com.alibaba.android.rimet', 'com.alibaba.android.rimet.fx', 'com.wemomo.bibi', 'com.tencent.weread']

fp = open('apps_category.json', 'r')
fp_result = fp.readlines()
fp_result = json.loads(fp_result[0])

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
			jSONObject3 = jSONObject.get('body')
			if jSONObject3 is not None:
				obj = jSONObject3.get('app_icon')
				if obj is not None and isinstance(obj, dict):
					jSONObject4 = obj
					for next in jSONObject4.keys():
						jSONArray2 = jSONObject4.get(next)
						if jSONArray2 is not None:
							for i in range(len(jSONArray2)):
								string = jSONArray2[i].get('logo')
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
	file= name + '.png'
	with open(file,'wb')as f:
		f.write(result.content)
	return result.status_code

def do_it(bundle_id):
	url = getIconUrl(bundle_id)
	if url is not None:
		download_it('out/' + bundle_id, url)
		print('%s : Success' % (bundle_id))
	else:
		print('%s : Failed' % (bundle_id))

def download_list(bundle_ids:list) -> None:
	with ThreadPoolExecutor(max_workers=16) as executor:
		executor.map(do_it,bundle_ids)

print(str(len(fp_result)) + ' third party icons in total:')
if not os.path.exists('out'):
	os.mkdir('out')
download_list(BASIC_APPS)
download_list(fp_result)

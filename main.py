from pytube import YouTube
from flask import *
import requests, math, os
from urllib.parse import quote
app = Flask(__name__)
app.config['MEDIA'] = 'mp3'
import math

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])
@app.route('/unduh/<path:filename>')
def unduh(filename):
	return send_from_directory(app.config['MEDIA'], filename, as_attachment=True)
@app.route('/',methods=['GET','POST'])
def yt2mp3():
	if  request.args.get('url'):
		try:
			yt = YouTube(request.args.get('url'))
		except:
			return {
				'status':False,
				'pesan':'Url Yg Anda Berikan Tidak Ada'
				}
		for i in yt.streams:
			if i.mime_type == 'audio/mp4':
				print('ditemukan')
				open('mp3/%s.mp3'%(i.title.replace('/','_')),'wb').write(requests.get(i.url).content)
				break
			else:
				pass
		return {
			'status':True,
			'title':i.title.replace('/','_'),
			'file_size':convert_size(i.filesize),
			'file':'/unduh/%s.mp3'%(quote(i.title))
			}
	else:
		return {
			'status':False,
			'pesan':'masukan parameter url'
			}
if __name__ == '__main__':
	if 'mp3' in os.listdir():
		pass
	else:
		os.mkdir('mp3')
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')))

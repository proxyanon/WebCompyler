'''
	@author Daniel Victor Freire Feitosa
	@version 2.0.0
	@license PL (private license)
	@copyrights All rights reserved to Daniel Victor Freire Feitosa - 2018
'''

from os import walk, path, makedirs, remove, _exit as osexit

try:
	from requests import post
except ImportError:
	print('module "requests" is needed try: python -m pip install requests and try run again')
	osexit(1)

try:
	import dukpy
except ImportError:
	print('module "dukpy" is needed try: python -m pip install dukpy and try run again')
	osexit(1)

from threading import Thread

''' WebCompyler is a tool to decrease your JS and CSS codes '''
class WebCompyler(Thread):

	__author__ = 'Daniel Victor Freire Feitosa'
	__version__ = '2.0.0'
	__license__ = 'GPL 3.0 (General Public License 3.0)'
	__github__ = 'https://github.com/proxyanon'

	def __init__(self, webpath, compile_js=True, compile_css=True, backup=True, excludes=['xml', 'scss', 'jsx', 'ts', 'txt', 'json', 'htaccess', 'h5'], verbose=False):

		Thread.__init__(self)
		self.api = {'css': 'https://cssminifier.com/raw', 'js': 'https://javascript-minifier.com/raw'}
		
		self.webpath = webpath
		self.compile_js = compile_js
		self.compile_css = compile_css
		self.backup = backup

		self.excludes = excludes
		self.ioupdates = ['html', 'php']
		self.backuppath = 'bkp_development'

		self.verbose = verbose
		self.running = True

		self.banner  = '\n █     █░▓█████  ▄▄▄▄    ▄████▄   ▒█████   ███▄ ▄███▓ ██▓███ ▓██   ██▓ ██▓    ▓█████  ██▀███  \n'
		self.banner += '▓█░ █ ░█░▓█   ▀ ▓█████▄ ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓██░  ██▒▒██  ██▒▓██▒    ▓█   ▀ ▓██ ▒ ██▒\n'
		self.banner += '▒█░ █ ░█ ▒███   ▒██▒ ▄██▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▓██░ ██▓▒ ▒██ ██░▒██░    ▒███   ▓██ ░▄█ ▒\n'
		self.banner += '░█░ █ ░█ ▒▓█  ▄ ▒██░█▀  ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██▄█▓▒ ▒ ░ ▐██▓░▒██░    ▒▓█  ▄ ▒██▀▀█▄  \n'
		self.banner += '░░██▒██▓ ░▒████▒░▓█  ▀█▓▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒▒██▒ ░  ░ ░ ██▒▓░░██████▒░▒████▒░██▓ ▒██▒\n'
		self.banner += '░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░▒▓▒░ ░  ░  ██▒▒▒ ░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░\n'
		self.banner += '  ▒ ░ ░   ░ ░  ░▒░▒   ░   ░  ▒     ░ ▒ ▒░ ░  ░      ░░▒ ░     ▓██ ░▒░ ░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░\n'
		self.banner += '  ░   ░     ░    ░    ░ ░        ░ ░ ░ ▒  ░      ░   ░░       ▒ ▒ ░░    ░ ░      ░     ░░   ░ \n'
		self.banner += '    ░       ░  ░ ░      ░ ░          ░ ░         ░            ░ ░         ░  ░   ░  ░   ░     \n'
		self.banner += '                      ░ ░                                     ░ ░                             \n\n'

		if path.exists(self.webpath) == False:
			print('IO Error {0} not exists'.format(self.webpath))
			self.running = False
		else:
			self.webpath = self.webpath.replace('/', '')

	''' compress using API from minfier.com '''
	def compress(self, read, _type):

		if self.running:
			try:
				if _type == 'js':
					read = dukpy.babel_compile(read)['code']
				else:
					read = read
				data = {'input': read}

				r = post(self.api[_type], data=data)
				if 'Error' in r.text:
					return read.strip()
				return r.text
			except:
				
				if self.verbose and self.running:
					print('[x] Error in compress verify your connection ...')
					self.running = False
				
				return read

	''' create the backup to develop '''
	def IOBakcup(self):

		if self.running and self.backup:
			
			if self.verbose:
				print('[+] Creating a backup ...')

			if path.exists(self.backuppath) == False:
				makedirs(self.backuppath)

			handles = [{'realpath': '{0}/{1}/{2}'.format(self.backuppath, paths, filename), 'paths': '{0}/{1}'.format(self.backuppath, paths), 'read': open('{0}\\{1}'.format(paths, filename), 'r').read()} for paths,dirs,files in walk(self.webpath) for filename in files]
			bkp_dirs = [handle['paths'] for handle in handles if path.exists(handle['paths']) == False]
			
			if len(bkp_dirs) > 0:
				create_bkp_dirs = [makedirs(bkp_dir) for bkp_dir in bkp_dirs]
			
			bkp = [open(handle['realpath'], 'w').write(handle['read']) for handle in handles]
	
	''' update the html and php files in way of the new compressed files '''
	def IOUpdate(self):

		if self.running:

			if self.verbose:
				print('[+] Updating html and php files ...')

			files = [filename for paths,dirs,files in walk(self.webpath) for filename in files for exclude in self.excludes if not exclude in filename if self.running]
			files_to_io = [filename for filename in files for ioupd in self.ioupdates if ioupd in filename if self.running]
			files_to_io = list(dict.fromkeys(files_to_io).keys())

			handles = [{'realpath': paths, 'read': open('{0}/{1}'.format(paths, filetoio), 'r')} for paths,dirs,files in walk(self.webpath) for filetoio in files_to_io for file in files if filetoio == file if self.running]
			files_resolved = [handle['read'].read() for handle in handles if self.running]
			closes = [handle['read'].close() for handle in handles if self.running]

			tmp_content = ''

			for index, content in enumerate(files_resolved):
				for row in content.split('\n'):
					
					if '<script' in row and 'src=' in row and '.min' not in row and self.running:
						to_search = row.split('src="')[1].split('">')[0]
						to_replace = to_search.replace('.js', '.min.js')
						row = row.replace(to_search, to_replace)

					if '<link' in row and 'href=' in row and '.min' not in row and self.running:
						to_search = row.split('href="')[1].split('">')[0]
						to_replace = to_search.replace('.css', '.min.css')
						row = row.replace(to_search, to_replace)

					tmp_content += '{0}\n'.format(row)

				
				try:
					to_search = tmp_content.split('<script type="text/javascript">')[1].split('</script>')[0]
					to_replace = self.compress(to_search, 'js')
					tmp_content = tmp_content.replace(to_search, to_replace)
				except:
					try:
						to_search = tmp_content.split('<script>')[1].split('</script>')[0]
						to_replace = self.compress(to_search, 'js')
						tmp_content = tmp_content.replace(to_search, to_replace)
					except:
						pass

				try:
					to_search = tmp_content.split('<style type="text/css">')[1].split('</style>')[0]
					to_replace = self.compress(to_search, 'css')
					tmp_content = tmp_content.replace(to_search, to_replace)
				except:
					try:
						to_search = tmp_content.split('<style>')[1].split('</style>')[0]
						to_replace = self.compress(to_search, 'css')
						tmp_content = tmp_content.replace(to_search, to_replace)
					except:
						pass

				handle = open('{0}/{1}'.format(handles[index]['realpath'], files_to_io[index]), 'w')
				handle.write(tmp_content.strip())
				handle.close()

				tmp_content = ''

	''' compressing the js and css files '''
	def IOCompress(self):

		if self.running:

			files = [filename for paths,dirs,files in walk(self.webpath) for filename in files for exclude in self.excludes if not exclude in filename and '.css' in filename or '.js' in filename if self.running]
			files = list(dict.fromkeys(files).keys())

			if self.compile_js:

				if self.verbose:
					print('[+] Compressing js ...')

				try:
					js_compresseds = [{'realpath': paths, 'file': file.replace('.js', '.min.js'), 'compressed': self.compress(open('{0}/{1}'.format(paths, file), 'r').read(), 'js'), 'to_remove': '{0}/{1}'.format(paths, file)} for paths,dirs,files in walk(self.webpath) for file in files for exclude in self.excludes if 'js' == file.split('.')[len(file.split('.'))-1] and 'min' not in file if self.running if self.compile_js and exclude not in file]
					handles = [{'writed': open('{0}/{1}'.format(js['realpath'], js['file']), 'w').write(js['compressed']), 'removed': remove(js['to_remove'])} for js in js_compresseds]
				except:
					pass

			if self.compile_css:

				if self.verbose:
					print('[+] Compressing css ...')
				
				try:
					css_compresseds = [{'realpath': paths, 'file': file.replace('.css', '.min.css'), 'compressed': self.compress(open('{0}/{1}'.format(paths, file), 'r').read(), 'css'), 'to_remove': '{0}/{1}'.format(paths, file)} for paths,dirs,files in walk(self.webpath) for file in files for exclude in self.excludes if 'css' == file.split('.')[len(file.split('.'))-1] in file and 'min' not in file if self.running if self.compile_css and exclude not in file]
					handles = [{'writed': open('{0}/{1}'.format(css['realpath'], css['file']), 'w').write(css['compressed']), 'removed': remove(css['to_remove'])} for css in css_compresseds]
				except:
					pass

	''' main function '''
	def run(self):

		if self.verbose:
			print(self.banner)

		Thread(target=self.IOBakcup,).start()
		Thread(target=self.IOUpdate,).start()
		Thread(target=self.IOCompress,).start()
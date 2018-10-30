from lib.core import WebCompyler as wc
from sys import argv, exit

path = ''
compile_ = ''

for index, arg in enumerate(argv):

	if arg == '--path' or arg == '-p' or arg == '-P':
		path = argv[index+1]

	if arg == '--compile' or arg == '-c' or arg == '-C':
		compile_ = argv[index+1]

if path == '' or compile_ == '':
	scriptname = argv[0].split('\\')[len(argv[0].split('\\'))-1]
	print('Uso: python {0} --path/-p/-P <pasta_do_projeto> --compile/-c/-C <all/css/js/none>'.format(scriptname))
	exit()

if compile_.lower() == 'all':
	compile_css = True
	compile_js = True
elif compile_.lower() == 'css':
	compile_css = True
	compile_js = False
elif compile_.lower() == 'js':
	compile_css = False
	compile_js = True
elif compile_.lower() == 'none':
	compile_css = False
	compile_js = False


if __name__ == '__main__':

	compyler = wc(webpath=path, compile_css=compile_css, compile_js=compile_js, verbose=True)

	compyler.start()
	compyler.join()
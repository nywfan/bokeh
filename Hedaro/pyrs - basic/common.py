import os
import stat

def remove_readonly(func, path, excinfo):
    """ force delete """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def Viewer(nburl=None, showcode=False, render='html'):

    from IPython.nbformat import reader as nbformat
    from IPython.nbconvert import exporters

	# Get url or file path
    if nburl:

        if nburl.startswith("http"):
            import requests
            response = requests.get(nburl)
            notebook = nbformat.reads_json(response.content)

        else:
            notebook = nbformat.read(fp=file(nburl))
        
    else:
        notebook = ''


	# Get rendering template
    if showcode:

        if render == 'html':
            template = 'full'
        
    else:

        if render == 'html':
            template = 'full2'


    import IPython.nbconvert
    from IPython.config import Config
    from IPython.nbconvert import HTMLExporter
    

    ## I use `basic` here to have less boilerplate and headers in the HTML.
	## we'll see later how to pass config to exporters.
    exportHtml = HTMLExporter(config=Config({'HTMLExporter':{'template_file':template}}))

    (body, resources) = exportHtml.from_filename(nburl)

    return body


def to_HTML(df):
    """ convert dataframes into an html table """

    df['link'] = '<a href=\"' + 'url?nburl=' + df['full'] + '\" target=\"_blank\">Report</a>' + """<b> | </b>""" + \
                 '<a href=\"' + 'url?showcode=True&nburl=' + df['full'] + '\" target=\"_blank\">Code</a>'                 
    
    df['update'] = """<button type="button" class="btn btn-primary" onclick="nbupdate(""" + "'" + df['repo2'] + "'" + """,""" + "'" + df['path2'] + "'" + """,""" + "'" + df['name'] + "'" + """,this);">Update """ + \
                   """</button>"""                            
    
    return df[['name', 'link', 'update']].to_html(index=False,escape=False, classes=['table table-condensed table-striped table-hover'])


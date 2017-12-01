import pandas as pd

def gentbl(d):
    df = pd.DataFrame(d, columns=['First Name', 'Last Name'])
    return df.to_html(index=False, classes='table table-hover table-bordered table-striped')

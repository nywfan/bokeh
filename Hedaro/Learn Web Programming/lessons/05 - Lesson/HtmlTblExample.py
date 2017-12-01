from pandas import DataFrame

def html():

        # Create a simple df
        df = DataFrame(data=[1,2,3,4,5], columns=['Revenue'])

        # Add columns
        df['bii'] = 'foo'
        df['Test'] = df['Revenue']*125
        df['Test1'] = df['Revenue']*125
        df['Test2'] = df['Revenue']*125
        df['Test3'] = df['Revenue']*125
        df['Test4'] = df['Revenue']*125

        return df.to_html(index=False, classes='table table-hover table-striped')



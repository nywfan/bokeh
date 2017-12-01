from pandas import DataFrame


def to_json(): 

        # Create a simple df
        df = DataFrame(data=[1,2,3,4,5], columns=['Revenue'])

        # Add a column
        df['bii'] = 'foo'

        return df.to_json()


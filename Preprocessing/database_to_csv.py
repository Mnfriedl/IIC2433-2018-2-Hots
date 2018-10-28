"""In this file, we will transform our complete database into a csv file, to make it easier to share.
"""

from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://hotsy:hotsy@localhost:5432/IIC2433-HOTSY')
a = pd.read_sql_query('select * from replay', con=engine)
a.to_csv('data.csv')

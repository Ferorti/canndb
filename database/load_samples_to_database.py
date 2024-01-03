import allel
import pandas as pd
import sqlite3
from config import DATABASE_NAME,VARIANTS_TABLE_NAME, vcf_files, vcf_path
import os



# Conectar a la base de datos
con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()

# Importante que hacer para no sobreescribir involuntariamente
if_exists = 'fail'


# Definir la ruta del archivo CSV
csv_path = os.path.join(SAMPLES_FOLDER, SAMPLES_CSV)

samples = pd.read_csv(csv_path, sep='\t')

samples.to_sql(name='Samples', con=con, if_exists=if_exists, index=False)

samples.to_sql('Samples', con=con)

con.close()
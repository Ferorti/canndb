import allel
import pandas as pd
import sqlite3
from config import DATABASE_NAME,VARIANTS_TABLE_NAME, vcf_files, vcf_path
import os

def vcf_to_df(vcf_file, fields='*', subset_columns=None):
    """
    Convierte un archivo VCF a un DataFrame de Pandas.

    Parámetros:
    - vcf_file (str): Ruta al archivo VCF.
    - fields (str, opcional): Campos a incluir en el DataFrame. Por defecto, '*'.

    Retorna:
    - pd.DataFrame: DataFrame que contiene los datos del VCF.
    """

    # Leer el archivo VCF como Pandas DataFrame
    df = allel.vcf_to_dataframe(vcf_file, fields='*')
    
    # Extraer las anotaciones provenientes de SnpEff
    snpEff_columns = ['allel', 'consequence', 'impact','gene','gid', 'type','tipoid','coding','tot','alt_nuc','alt_prot','cdnapos', 'cdspos','ppos','distance','error']
    annotations = df.ANN.str.split('|', expand=True)
    annotations.columns = snpEff_columns
    
    # Unir las variatnes con las anotaciones
    df = pd.concat([df,annotations], axis=1)
    df.columns = df.columns.str.lower()


    return df
    
# Conectar a la base de datos
con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()

for vcf_file in vcf_files:
    sample = vcf_file.split('.')[0]

    try:
        # Convertir VCF en DataFrame de Pandas
        df = vcf_to_df(os.path.join(vcf_path,vcf_file))

        # Agregar la columna sample_id al DataFrame
        df['sample_id'] = sample

        # Cargar datos en la base de datos
        df.to_sql(VARIANTS_TABLE_NAME, con=con, if_exists='append')

        print(f'Se cargaron {len(df)} variantes en {VARIANTS_TABLE_NAME} en {DATABASE_NAME}')

    except Exception as e:
        print(f'Error en la muestra {sample}')
        print(e, end='\n')

    finally:
        con.close()
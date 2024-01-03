# Variables de configuracion para la carga de variantes a partir de archivos VCFs Anotados
import os
import sqlite3



SAMPLES_FOLDER = 'samples'
SAMPLES_CSV = 'samples.tsv'

vcf_path = "./vcfs"
vcf_files = [i for i in os.listdir(vcf_path) if i.endswith('vcf.gz')]

#samples = [vcf_file.split(".")[0] for vcf_file in vcf_files]

DATABASE_NAME = "./canndb.db"
VARIANTS_TABLE_NAME = 'variants'
SAMPLES_TABLE_NAME = 'Samples'




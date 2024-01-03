import sqlite3
import pandas as pd



columns = [
        
        "sample_id", 'chrom', 'pos', 'id', 'ref', 'alt_1', 'alt_2', 'alt_3','qual', 'baseqranksum','readposranksum', 'ann', #generales
        
        'allel', 'consequence', 'impact','gene','gid', 'type','tipoid','coding','tot','alt_nuc','alt_prot','cdnapos', 'cdspos','ppos','distance','error' # SnpEff
        
        ]

def filter_variants(params, limite=100, offset=0):
    
    conn = sqlite3.connect('../database/canndb.db')

    sql_query = f"SELECT {', '.join(columns)} FROM variants WHERE "

    conditions = []

    for clave, valor in params.items():
        if ',' in valor:
            # Si el valor contiene comas, usar IN en lugar de igualdad
            values = [f"'{v.strip()}'" for v in valor.split(',')]
            conditions.append(f"{clave} IN ({', '.join(values)})")
        else:
            conditions.append(f"{clave}='{valor}'")

    if params:
        sql_query += " AND ".join(conditions)
    
    if limite:
        sql_query += f" LIMIT {limite} OFFSET {offset}"

    print(sql_query)

    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn.close()

    return pd.DataFrame(result, columns=columns)




def filter_samples(params, limite=100, offset=0):
    
    conn = sqlite3.connect('../database/canndb.db')

    sql_query = f"SELECT * FROM Samples WHERE "

    conditions = []

    for clave, valor in params.items():
        if ',' in valor:
            # Si el valor contiene comas, usar IN en lugar de igualdad
            values = [f"'{v.strip()}'" for v in valor.split(',')]
            conditions.append(f"{clave} IN ({', '.join(values)})")
        else:
            conditions.append(f"{clave}='{valor}'")

    if params:
        sql_query += " AND ".join(conditions)
    
    if limite:
        sql_query += f" LIMIT {limite} OFFSET {offset}"


    cursor = conn.cursor()

    cursor.execute(sql_query)

    column_names = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    conn.close()

    return pd.DataFrame(result, columns=column_names)


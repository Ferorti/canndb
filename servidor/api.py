from flask import Blueprint, request
import sqlite3
import pandas as pd
from flask_apispec.annotations import doc
from flask_apispec import use_kwargs
from webargs import fields
from query import filter_variants, filter_samples


restapi = Blueprint('api', __name__)


@restapi.route("/getVariants", methods=['GET'])
@doc(tags=['Genomic variants'],description=(
        "Filter variants"
    )
)
@use_kwargs(   
    {'sample_id': fields.Str(description="Sample name"),
    'gid': fields.Str(description="Gene ID"),
    'chrom': fields.Str(description="Chromosome"),
    'pos': fields.Str(description="Alt position"),
    'consequence': fields.Str(description="Consequence of variant"),
    'impact': fields.Str(description="Impact of variant (High, Moderate, Low, Modifier)"),
    'limite': fields.Str(description="Max variants (Default 1000)"),
    'page': fields.Str(description="Page for pagination (Default 0)"),
    }
, location='query')
def get_variants(**kwargs):

    params = request.args.to_dict()


    limite = 1000 # Default maximo 1000 variantes por consulta
    if  params.get('limite'):
        lim = params.pop('limite')
        limite = int(lim)

    offset = 0 # Offset para pagination, default 0
    if  params.get('page'):
        off = params.pop('page')
        offset = int(off) * limite


    if params.get('impact'):
        params['impact'] = params['impact'].upper()

    try:

        df = filter_variants(params, limite=limite, offset= offset)



        output_columns = ['sample_id', "gid", 'chrom', 'pos', 'alt_nuc', 'alt_prot','coding', 'consequence', 'impact']
        df = df[output_columns]


        return {
            'parameters':params,
            'n_results':len(df),
            'variants':df.head(100).to_dict('records')
        }

    except sqlite3.OperationalError :
        return {'message':'Bad requests, check parameters', 'parameters':params}




@restapi.route("/getSamples", methods=['GET'])
@doc(tags=['Cultivar Samples'],description=(
        "Filter variants"
    )
)
@use_kwargs(   
    {'sample_id': fields.Str(description="Sample name"),
    'name': fields.Str(description="Sample name"),
    'strain': fields.Str(description="Strain"),
    #'description': fields.Str(description="Short description"),
    #'annotations': fields.Str(description="Annotations"),
    'sex': fields.Str(description="Sex"),
    'cultivation_date': fields.Str(description="Date of plant cultivation"),
    'cultivar': fields.Str(description="CUltivar (Default canndico)"),
    }
, location='query')
def get_samples(**kwargs):

    try:
        print(kwargs)
        df = filter_samples(kwargs)
        return df.fillna("").to_dict("records")
    
    except Exception as e:
        return {'message': 'Error processing samples', 'error': str(e)}
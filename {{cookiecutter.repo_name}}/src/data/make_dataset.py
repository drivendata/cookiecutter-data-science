# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import yaml
import ssl
import vertica_python
import sys
import subprocess
import re
from jinja2 import Template


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


if run_from_ipython():
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("matplotlib inline")
    project_dir = os.getcwd()
else:
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
src_dir = os.path.join(project_dir, "src")
sys.path.append(src_dir)


def get_vertica_python_conn(cfg=None):
    cfg = cfg or default_cfg
    params = {
        'host': cfg['host'],
        'port': 5433,
        'database': cfg['database'],
        'read_timeout': 600,
        'unicode_error': 'strict',
        'password': cfg['password'],
        'user': cfg['user']}
    if 'VERTICA_NO_SSL' not in cfg.keys():
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.check_hostname = False
        params['ssl'] = ssl_context
    conn = vertica_python.connect(**params)
    return conn


def vertica_python_conn_yaml(config, account='user', server='vertica'):
    """
    Generate vertica_python configuration object from configuration.

    Args:
    config -- database configuation.

    Returns:
    conn -- database connection.
    """
    params = {
        'host': config[server]['host'],
        'port': 5433,
        'database': config[server]['database'],
        'read_timeout': 10 * 60 * 60,
        'unicode_error': 'strict',
        'user': config[server][account]['username'],
        'password': config[server][account]['password']
    }
    conn = vertica_python.connect(**params)
    return conn


def vertica_python_conn_env(config, account='user', server='vertica'):
    """
    Generate vertica_python configuration object from configuration.

    Args:
    config -- database configuation.

    Returns:
    conn -- database connection.
    """
    params = {
        'host': os.environ.get("_".join([server, "host"])),
        'port': 5433,
        'database': os.environ.get("_".join([server, "database"])),
        'read_timeout': 10 * 60 * 60,
        'unicode_error': 'strict',
        'user': os.environ.get("_".join([server, account, "username"])),
        'password': os.environ.get("_".join([server, account, "password"]))
    }
    conn = vertica_python.connect(**params)
    return conn


def vertica_python_conn_wrapper(**kwargs):
    # first, look for the YAML
    if find_dotenv('.config.yml'):
        conn_info = yaml.safe_load(open(find_dotenv('.config.yml')))
        return vertica_python_conn_yaml(conn_info, **kwargs)
    # else, look for the bash script
    elif find_dotenv('.config.sh'):
        load_dotenv(find_dotenv('.config.sh'))
        return vertica_python_conn_env(**kwargs)
    # else, assume they are in the environment already
    else:
        return vertica_python_conn_env(**kwargs)


def strip_comments(x: str):
    """Remove SQL comments from a string."""
    return re.sub("--.*?\n", "\n", x)


def single_line(x: str):
    """Convert a sql command into a single line (remove newlines)."""
    return re.sub(r'\s*\n+\s*', ' ', x)


def csv_command(query: str,
                outfile: str,
                header: bool=False):
    """Generate command line command for passing `query` into vsql
    and directing the output to `outfile`."""
    # print(os.environ.get("pw"))
    if header:
        return """/usr/local/bin/vsql
                  -h vertica.private.massmutual.com
                  -d advana
                  -U {0}
                  -w '{1}'
                  -F $'|'
                  -A
                  -c "{2}" |
                  gzip -c > data/raw/{3}""".format(os.environ.get("user"),
                                                   os.environ.get("pw"),
                                                   query,
                                                   outfile)
    else:
        return """/usr/local/bin/vsql
                  -h vertica.private.massmutual.com
                  -d advana
                  -U {0}
                  -w '{1}'
                  -F $'|'
                  -At
                  -c "{2}" |
                  gzip -c > data/raw/{3}""".format(os.environ.get("user"),
                                                   os.environ.get("pw"),
                                                   query,
                                                   outfile)


def vsql_to_csv(query: str,
                outfile: str,
                header: bool=False):
    """Run query and direct output to outfile."""
    command = csv_command(single_line(strip_comments(query)),
                          outfile,
                          header=header)
    print(command)
    subprocess.call(command, shell=True)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    with open(input_filepath, "r") as f:
        query = f.read()

    df = pd.read_sql_query(query, con)
    df.to_pickle(output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    # this will work if user and pw are defined in the root .env
    conn_info = {'host': 'vertica.private.massmutual.com',
                 'port': 5433,
                 'user': os.environ.get("user"),
                 'password': os.environ.get("pw"),
                 'database': 'advana',
                 # 100 minutes timeout on queries
                 'read_timeout': 6000,
                 # default throw error on invalid UTF-8 results
                 'unicode_error': 'strict',
                 # SSL is disabled by default
                 'ssl': True}

    con = get_vertica_python_conn(conn_info)

    # OR

    con = vertica_python_conn_wrapper()

    main()

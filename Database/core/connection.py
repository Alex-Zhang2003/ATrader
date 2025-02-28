from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.paths import CRED_PATH
import pandas as pd
import json


def get_login_info(path=''):
    with open(CRED_PATH, 'r') as f:
        data = json.load(f)
    return data


def create_connection_str(username, password, port):
    return f'postgresql://{username}:{password}@atrader-db-atrader.g.aivencloud.com:{port}/defaultdb'


def create_conn_engine():
    login_info = get_login_info()
    conn_str = create_connection_str(login_info['user'], login_info['pw'], login_info['port'])
    engine = create_engine(conn_str)
    return engine


def create_session(engine):
    return sessionmaker(bind=engine)

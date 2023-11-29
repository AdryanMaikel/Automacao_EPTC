# -*- coding: utf-8 -*-

import os
from shutil import move
from bs4 import BeautifulSoup
from dboracle import get_protocols

DIR_ACTUAL = os.getcwd().replace('\\', '/')
DIR_TEMP = f'{DIR_ACTUAL}/temp/'

USER_PATH = os.path.expanduser('~').replace('\\', '/')
DIR_DOWNLOAD = f'{USER_PATH}/Downloads'
FILENAME = 'protocolos_por_fila'

REFACTOR_SERVICES = lambda service: service.split(' - ')[-1]
REFACTOR_ADDRESSS = lambda address: address.split(' ,')[0]
REFACTOR_PROTOCOL = lambda protocol: protocol.replace('\n', '')

def clear_dir_download():
  """Limpa do diretório de downloads todos arquivos que sejam 
  'protocolos_por_fila...'

  Returns:
    message [color(str), message:(str)]: Mensagem de sucesso ou falha
  """
  try:
    for file in os.listdir(DIR_DOWNLOAD):
      if file.startswith(FILENAME):
        os.remove(f'{DIR_DOWNLOAD}/{file}')
    return ['green', 'Diretório limpo!']
  except:
    return ['red', 'Falha ao limpar diretório de downloads.']


def move_excel(lote: str):
  try:
    move(f'{DIR_DOWNLOAD}/{FILENAME}.xls', f'{DIR_TEMP}{lote}')
    return 'atualizado com sucesso'
  except:
    return 'não encontrado'


def read_excel(excel: str):
  lote = 'LOTE 1' if excel == 'LOTE_1.xls' else 'LOTE 2'
  try:
    dir_file = f'{DIR_TEMP}{excel}'
    with open(dir_file, 'r', encoding='latin-1') as file:
      file_readed = BeautifulSoup(file.read(), 'html.parser')
      return extract_values_of_excel(lote, file_readed)
  except:
    return ['red', 'Arquivo não encontrado']


def extract_values_of_excel(LOTE: str, EXCEL_READED: BeautifulSoup):
  RECLAMATIONS = {
    'PROTOCOLO': [],
    'RECLAMANTE': [],
    'SERVIÇO': [],
    'ENDEREÇO': [],
    'DATA_ABERTURA': [],
    'DATA_VENCIMENTO': [],
    'PRAZO_DIAS': [],
    'ATRASO_DIAS': [],
  # 'LOTE': [],
  # 'DESCRIÇÃO': []
  }

  KEYS, TDS = RECLAMATIONS.keys(), EXCEL_READED.find_all('td')

  for i, key in enumerate(KEYS):
    values = [str(td.text).strip().upper() for td in TDS[i::8]]
    RECLAMATIONS[key] = values

  TOTAL = len(RECLAMATIONS['PROTOCOLO'])
  for key in KEYS:
    if len(RECLAMATIONS[key]) != TOTAL:
      return [
        'red', f'{key}: {len(RECLAMATIONS[key])} não bateu com {TOTAL}'
      ]

  RECLAMATIONS['PROTOCOLO'] = list(
    map(REFACTOR_PROTOCOL, RECLAMATIONS['PROTOCOLO'])
  )
  RECLAMATIONS['SERVIÇO'] 	= list(
    map(REFACTOR_SERVICES, RECLAMATIONS['SERVIÇO'])
  )
  RECLAMATIONS['ENDEREÇO']  = list(map(
    REFACTOR_ADDRESSS, RECLAMATIONS['ENDEREÇO'])
  )
  RECLAMATIONS['LOTE'] = [LOTE] * TOTAL
  
  DB_PROTOCOLS = get_protocols()
  
  index_protocol_contains = []
  for index, protocol in enumerate(RECLAMATIONS['PROTOCOLO']):
    if protocol in DB_PROTOCOLS:
      index_protocol_contains.append(index)
  
  for index in index_protocol_contains:
    for key in RECLAMATIONS:
      del RECLAMATIONS[key][index]
  
  with open(f'{DIR_ACTUAL}/reclamations.py', 'w', encoding='utf-8') as file_reclamations:
    file_reclamations.write(f'RECLAMATIONS = {str(RECLAMATIONS)}')
  
  return ['green', 'Sucesso!']


def merged_excels(LOTE_1: dict, LOTE_2: dict):
  LOTE_1_KEYS, LOTE_2_KEYS = LOTE_1.keys(), LOTE_2.keys()
  if LOTE_1_KEYS == LOTE_2_KEYS:
    RECLAMATIONS = {}
    for key in LOTE_1_KEYS:
      RECLAMATIONS[key] =  LOTE_1[key] + LOTE_2[key]
    return RECLAMATIONS
  else:
    return f'Lote 1 tem {len(LOTE_1_KEYS)} chaves e '+\
      f'lote 2 tem {len(LOTE_2_KEYS)} chaves.'


if __name__ == '__main__':
  # print(clear_dir_download())
  print(read_excel('LOTE_1.xls'))
  pass

# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from excel import (
  DIR_TEMP, contains_excel_in_dir_download, clear_dir_download, move_excel)
from login import USER, PASSWORD
import json

URL_EPTC = f'https://{USER}:{PASSWORD}@156poa.procempa.com.br'
URL_FILA = f'{URL_EPTC}/sistemas/156/fila/servicos_local.php?'
LOTE_1, LOTE_2 = '999901074', '999901075'
URL_EXCEL_LOTE_1 = f'{URL_FILA}cod_local_destino={LOTE_1}'
URL_EXCEL_LOTE_2 = f'{URL_FILA}cod_local_destino={LOTE_2}'
XPATH_BUTTON_DOWNLOAD_EXCEL = '//html/body/table/tbody/tr[1]/th[2]/a'
FIREFOX = Firefox

URL_FIND_PROTOCOL = (
  f'{URL_EPTC}/Sistemas/156/fila/fila_01.php?modo=4&protocolo=')
XPATH_DETALHES_TRAMITES = '//html/body/table[4]/tbody/tr/td/a[1]'
XPATH_TEXTAREA = '//textarea'
URL_INFO_TRAMITE = (
  f'{URL_EPTC}/Sistemas/156/fila/visualiza_info.php?protocolo=')
RESTANT = '&seq_tramita=0&fase=0&cod_tramite=0'

FILE_NAME = 'dados.json'

def start_firefox():
  """Função para abrir o navegador firefox e ir até o site da EPTC

  Returns:
    webdriver.Firefox: Retorna o navegador firefox
  """
  BROWSER = FIREFOX()
  BROWSER.get(URL_EPTC)
  return BROWSER


def goto_url_download(URL_LOTE: str):
  """Função que abre o site da EPTC, baixa o excel e fecha o navegador
  
  Args:
  	URL_LOTE (str): Baixa a planilha com base no lote
  
  Returns:
  	[color, text]: a cor a ser preenchida e mensagem de falha ou sucesso
  """
  try:
    BROWSER = start_firefox()
    BROWSER.get(URL_LOTE)
    BROWSER.find_element(By.XPATH, XPATH_BUTTON_DOWNLOAD_EXCEL).click()
    close_firefox(BROWSER)
    return ['green', 'Sucesso!']
  except:
    return ['red', 'Falha ao baixar.']


def download_excel(lote: int):
  """Função para ir até o site da Eptc e baixar as planilhas do excel 
  para extrair os dados das mesmas.
  
  Args:
  	lote (int): Número do lote para baixar a planilha
  
  Returns:
  	[color, text]: a cor a ser preenchida e mensagem de falha ou sucesso
  """
  clear_dir_download()
  moved  = ''
  match lote:
    case 1:
      goto_url_download(URL_EXCEL_LOTE_1)
      if contains_excel_in_dir_download():
        moved = move_excel('LOTE_1.xls')
    case 2:
      goto_url_download(URL_EXCEL_LOTE_2)
      if contains_excel_in_dir_download():
        moved = move_excel('LOTE_2.xls')
    case _ :
      return ['red', 'Falha ao baixar excel!']
  return ['green', f'Excel LOTE {lote} {moved}!']


def get_informations_from_reclamation(RECLAMATIONS: dict):
  """Função que pega todos os dados de cada protocolo das reclamações e
  cria um arquivo json contendo todos os dados
  
  Args:
  	RECLAMATIONS (dict): Dados dos excels contendo as reclamações
  
  Returns:
  	[color, text]: a cor a ser preenchida e mensagem de falha ou sucesso
  """
  
  PROTOCOLS = RECLAMATIONS['PROTOCOLO']
  INFORMATIONS_PROTOCOL = {
    'STPOA_LINHA': [],
    'STPOA_SENTIDO': [],
    'STPOA_PREFIXO': [],
    'STPOA_MOTIVO': [],
    'STPOA_DATA': [],
    'STPOA_HORA': [],
    'DESCRIÇÃO': []
  }

  INFORMATIONS_KEYS = INFORMATIONS_PROTOCOL.keys()
  TOTAL = len(PROTOCOLS)

  if TOTAL > 0:
    BROWSER = start_firefox()
    for protocol in PROTOCOLS:
      try:
        BROWSER.get(f'{URL_FIND_PROTOCOL}{protocol}')
        BROWSER.find_element(By.XPATH, XPATH_DETALHES_TRAMITES).click()
        text = BROWSER.find_element(By.XPATH, XPATH_TEXTAREA).text
        INFORMATIONS_PROTOCOL['DESCRIÇÃO'].append(text)
      except:
        return ['red', 'Baixe a planilha novamente!']
      try:
        BROWSER.get(f'{URL_INFO_TRAMITE}{protocol}{RESTANT}')
        for key in INFORMATIONS_KEYS:
          if key == 'DESCRIÇÃO':
            break
          td = BROWSER.find_element(By.XPATH, f"//td[text()='{key}']")
          text = td.find_element(By.XPATH, 'following-sibling::td').text
          INFORMATIONS_PROTOCOL[key].append(text)
      except:
        return ['red', 'Baixe a planilha novamente!']
    close_firefox(BROWSER)
    for key in INFORMATIONS_KEYS:
      TOTAL_KEY = len(INFORMATIONS_PROTOCOL[key])
      if TOTAL != TOTAL_KEY:
        return f'Total não bate! {key} com {TOTAL_KEY} valores é difer'+\
          f'ente de {TOTAL}.'
      else:
        RECLAMATIONS[key] = INFORMATIONS_PROTOCOL[key]
    
    try:
      with open(f'{DIR_TEMP}{FILE_NAME}', 'w', encoding='utf-8') as FILE:
        json.dump(RECLAMATIONS, FILE, indent=2, ensure_ascii=False)
      return ['green', 'Dados salvos com sucesso!']
    except:
      return ['red', 'Falha ao salvar os dados.']


def close_firefox(browser: Firefox):
  """Função para fechar o navegador Firefox já aberto antes

  Args:
    browser (Firefox): Navegador aberto pelafunção start_firefox

  Returns:
    message (str): Falha ou Sucesso!
  """
  try:
    browser.quit()
    return 'Firefox fechado com sucesso.'
  except:
    return 'Falha ao fechar o Firefox.'


if __name__ == '__main__':
  pass

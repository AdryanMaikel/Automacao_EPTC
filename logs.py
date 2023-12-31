from datetime import datetime

from directories import DIR_LOGS
DIR_FILE_LOGS = f'{DIR_LOGS}ngAutomacaoEptc.log'

def write_log(message):
  '''Função para escrever os detalhes do processo da execução do programa

  Args:
    message (str): mensagem a ser inserida
  '''
  NOW = datetime.now()
  DATE_FORMAT = NOW.strftime('%Y-%m-%d %H:%M:%S')
  with open(DIR_FILE_LOGS, 'a', encoding='utf-8') as FILE_LOGS:
    FILE_LOGS.write(f'{DATE_FORMAT} : {message}\n')


if __name__ == '__main__':
  pass
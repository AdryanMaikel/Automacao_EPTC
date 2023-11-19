from PySimpleGUI import (
  Window, theme, WINDOW_CLOSED, Push, Button, Text, HSep, VSep)
  
from browser import start_firefox, close_firefox, download_excel

theme('Gray Gray Gray')
browser, LAYOUT = None, [
  [Text('Pegar reclamações da EPTC'), Push()],
  [
    Push(),
    Button('Abrir Firefox', size=(18, 1), disabled=False),
    Button('Fechar Firefox', size=(18, 1), disabled=True),
    Push()
  ],
  [Text(text='', key='response firefox', visible=False)],
  [HSep()],
  [Text('Baixar as planilhas.'), Push()],
  [
    Button('LOTE 1', size=(7, 1), disabled=True),
    Button('LOTE 2', size=(7, 1), disabled=True)
  ],
  [],
]
WINDOW = Window('EPTC', LAYOUT)

while True:
  events, values = WINDOW.read()
  
  if events == 'Abrir Firefox':
    browser = start_firefox()
    WINDOW['Abrir Firefox'].update(disabled=True)
    WINDOW['Fechar Firefox'].update(disabled=False)
    WINDOW['LOTE 1'].update(disabled=False)
    WINDOW['LOTE 2'].update(disabled=False)
  
  if events == 'Fechar Firefox':
    response = close_firefox(browser)
    browser = None
    WINDOW['response firefox'].update(response)
    WINDOW['response firefox'].update(visible=True)
    WINDOW['Abrir Firefox'].update(disabled=False)
    WINDOW['Fechar Firefox'].update(disabled=True)
    WINDOW['LOTE 1'].update(disabled=False)
    WINDOW['LOTE 2'].update(disabled=False)
    
  if events == 'LOTE 1':
    download_excel(browser, 1)
  
  if events == 'LOTE 2':
    download_excel(browser, 2)

  if events == WINDOW_CLOSED:
    break

WINDOW.close()

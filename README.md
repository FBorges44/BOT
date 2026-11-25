
# Automação de laudos — guia passo a passo

Este projeto é um MVP para demonstrar o preenchimento automático de um
formulário **local de teste** usando Python, Playwright e dados de um arquivo
JSON.

> **Importante:** os dados fornecidos são fictícios. Este MVP não calcula nem
> emite um laudo técnico, não acessa o sistema da CAIXA e não salva ou envia o
> formulário. A análise, os valores e a aprovação do laudo devem ser feitos por
> um profissional habilitado. Sempre revise os campos antes de qualquer uso.

## 1. O que o robô faz

Ao executar `init-agente.bat`, o programa:

1. Lê os valores padrão de `data/dados_laudo.json`.
2. Abre o formulário local `formulario-teste.html` no Chromium.
3. Identifica os elementos do formulário e registra a lista em
   `data/campos_extraidos.json`.
4. Preenche os campos compatíveis com os valores do JSON.
5. Confere se os valores preenchidos correspondem aos valores de entrada.
6. Salva o resultado da validação em `data/resultado_automacao.json` e uma
   captura de tela em `logs/laudo_preenchido.png`.
7. Mantém o navegador aberto para revisão. Pressione Enter no terminal para
   fechá-lo.

O comando é executado sob demanda: execute-o novamente sempre que quiser
preencher o formulário de novo. Não é um agente que fica rodando em segundo
plano.

## 2. Requisitos

- Windows 10 ou 11.
- Python 3 instalado e disponível pelo comando `py` ou `python`.
- Visual Studio Code (recomendado).
- Acesso à internet durante a instalação das dependências e do navegador do
  Playwright.

Para verificar se o Python está instalado, abra o PowerShell ou o terminal do
VS Code e execute:

```powershell
py --version
```

Se `py` não for reconhecido, tente:

```powershell
python --version
```

Se nenhum dos comandos funcionar, instale o Python pelo site oficial
<https://www.python.org/downloads/>. Durante a instalação, habilite a opção
para adicionar o Python ao `PATH`; depois, feche e reabra o terminal.

## 3. Abrir a pasta do projeto

No VS Code, escolha **Arquivo > Abrir Pasta** e abra a pasta `BOT` que contém
`requirements.txt`, `crawler` e `automation`.

Ou abra um terminal e navegue até a pasta do projeto. Ajuste o caminho para o
local onde os arquivos estão salvos:

```powershell
cd "C:\caminho\para\BOT"
code .
```

Confirme que está na pasta certa:

```powershell
Get-ChildItem
```

Você deve encontrar, entre outros, `requirements.txt`, `init-agente.bat`,
`formulario-teste.html`, `crawler` e `data`.

## 4. Criar e ativar o ambiente Python

Crie um ambiente virtual isolado para as dependências do projeto:

```powershell
py -m venv venv
```

Se o comando `py` não estiver disponível, use:

```powershell
python -m venv venv
```

Ative o ambiente no PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação por política de execução, permita scripts
apenas nesta janela e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Quando ativado, normalmente aparece `(venv)` no início da linha do terminal.
Você também pode executar o arquivo `init-agente.bat` sem ativar o ambiente,
pois ele usa diretamente o Python que está dentro de `venv`.

## 5. Instalar as dependências

Com o terminal na pasta `BOT`, atualize o instalador de pacotes e instale as
bibliotecas listadas em `requirements.txt`:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Instale também o Chromium usado pelo Playwright:

```powershell
python -m playwright install chromium
```

Esses passos são necessários na primeira configuração do ambiente. Se apagar
a pasta `venv` ou criar um ambiente virtual novo, repita-os.

## 6. Configurar o comportamento

O arquivo `.env` controla opções de execução. Se ele ainda não existir, crie
uma cópia do modelo:

```powershell
Copy-Item .env.example .env
```

Para exibir o navegador durante o preenchimento, deixe esta configuração:

```dotenv
BROWSER_HEADLESS=false
```

Com `BROWSER_HEADLESS=true`, o navegador roda oculto; use essa opção somente
quando não precisar revisar visualmente os campos.

## 7. Conferir ou alterar os valores padrão

Abra `data/dados_laudo.json`. Os valores de exemplo são fictícios:

```json
{
  "imovel": {
    "municipio": "Teresina",
    "estado": "PI",
    "endereco": "Rua Exemplo, 100",
    "tipo_imovel": "Residencial",
    "area_construida": "120.50",
    "area_terreno": "250.00"
  },
  "avaliacao": {
    "padrao_construtivo": "Médio",
    "estado_conservacao": "Bom",
    "observacoes": "Imóvel utilizado para teste de automação."
  }
}
```

Edite os valores mantendo a estrutura e os nomes das propriedades. Eles
correspondem aos atributos `name` do formulário HTML; se renomear uma
propriedade, o nome correspondente no formulário também precisa ser ajustado.
Valores de opções (`select`), como `tipo_imovel` e `padrao_construtivo`, devem
corresponder a uma opção disponível no formulário.

Mantenha o JSON válido: use aspas duplas nas chaves e nos textos, separe os
itens por vírgulas e não deixe vírgula depois do último item. Os números de
área são representados como texto com ponto decimal.

## 8. Executar o preenchimento

No terminal do VS Code, já na pasta do projeto, execute:

```powershell
.\init-agente.bat
```

Também é possível dar dois cliques em `init-agente.bat` no Explorador de
Arquivos. O próprio comando entra na pasta do projeto e usa o ambiente
`venv`; não é necessário iniciar outro terminal para o servidor do formulário.

Para iniciar diretamente pelo Python, com o ambiente ativado, use:

```powershell
python -m crawler.crawler
```

## 9. Revisar e finalizar a execução

Depois que a automação preencher os campos:

1. Confira visualmente todos os valores no navegador.
2. Confira o arquivo `data/resultado_automacao.json`; o campo `"sucesso"`
   deverá estar como `true`, e cada campo preenchido e validado deverá aparecer
   como `true`.
3. Se algo estiver incorreto, feche o navegador pressionando Enter no
   terminal, corrija os valores em `data/dados_laudo.json` e execute novamente.
4. A captura da tela fica em `logs/laudo_preenchido.png`.
5. Pressione Enter no terminal para fechar o navegador.

**O robô não clica no botão “Salvar laudo”.** A execução termina após preencher
e validar os campos, deixando a revisão sob responsabilidade do usuário.

## 10. Arquivos importantes

| Caminho | Finalidade |
| --- | --- |
| `init-agente.bat` | Atalho para iniciar o preenchimento no Windows. |
| `data/dados_laudo.json` | Fonte dos dados padrão que serão preenchidos. |
| `formulario-teste.html` | Formulário local fictício usado para testar o MVP. |
| `crawler/browser.py` | Inicialização e encerramento do Chromium. |
| `crawler/navigation.py` | Navegação até o formulário. |
| `crawler/extractor.py` | Identificação e registro dos elementos do formulário. |
| `automation/preencher.py` | Preenchimento dos campos compatíveis. |
| `crawler/crawler.py` | Fluxo principal, validação e gravação dos resultados. |
| `data/campos_extraidos.json` | Elementos HTML identificados na página. |
| `data/resultado_automacao.json` | Resultado do preenchimento e da validação. |
| `logs/laudo_preenchido.png` | Captura do formulário após o preenchimento. |

## 11. Solução de problemas

### `venv\Scripts\python.exe` não encontrado

Na pasta `BOT`, crie o ambiente virtual e instale as dependências:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### Erro indicando que o Chromium não está instalado

Com o ambiente virtual ativado, execute:

```powershell
python -m playwright install chromium
```

### Erro ao ler `dados_laudo.json`

Confira se o arquivo existe em `data`, se o conteúdo é JSON válido e se foram
mantidas as chaves `imovel` e `avaliacao`.

### Campo não encontrado ou opção incompatível

Confira se o nome da propriedade em `data/dados_laudo.json` é igual ao
atributo `name` do elemento correspondente em `formulario-teste.html`. Para
campos de seleção, confira se o texto corresponde a uma das opções disponíveis.

### O navegador não aparece

Confira se `.env` contém `BROWSER_HEADLESS=false`. Feche e execute o comando
novamente.

### A validação falhou

Veja quais campos aparecem como `false` em `data/resultado_automacao.json`.
Confira os nomes e valores no JSON e no HTML, corrija o que for necessário e
rode novamente.

## 12. Limites e próximos passos

Esta versão automatiza somente o formulário local de demonstração. Ela não
percorre telas de outros sistemas, não lê documentos PDF ou Excel, não
consulta fontes de dados e não está integrada ao sistema da CAIXA. Também não
calcula valores de avaliação nem substitui vistoria, análise técnica ou
aprovação de um engenheiro.

Uma integração real exigiria mapear e testar cada tela e campo, definir as
fontes dos dados, tratar autenticação e erros e validar o fluxo com autorização
e supervisão apropriadas. Até essa etapa ser implementada e validada, use
apenas o formulário local de teste.
=======

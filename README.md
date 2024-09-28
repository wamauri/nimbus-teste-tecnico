
---

# Nimbus Meteorologia - Teste Técnico Python PL
![alt text](image-1.png)
## Geral
Este repositório tem duas aplicações Python como parte do teste técnico da Nimbus. As aplicações são projetadas para lidar com a recepção contínua de dados e geração de relatórios com base em informações meteorológicas. O projeto utiliza comunicação TCP/IP para recepção de dados e geração de relatórios meteorológicos em formato PDF, que também podem ser enviados por e-mail de forma automática por meio de um comando.

## Tabela de Conteúdo
- [Geral](#Geral)
- [Features](#features)
- [Tecnologias](#tecnologias)
- [Instruções](#instruções)
- [Executando aplicações](#executando-aplicações)
  - [Applicação 1: Serviço Continuo de Receptação de Dados](#applicação-1-serviço-continuo-de-receptação-de-dados)
  - [Applicação 2: Gerador de Relatório Meteorológico](#applicação-2-gerador-de-relatório-meteorológico)
- [Contato](#contato)

## Features

### 1. Serviço Continuo de Receptação de Dados
- **Execução Contínua** até a interrupção manual.
- **Recebe dados** via TCP/IP na porta 5784.
- **Validação dos Dados** formato: `name,email,phone,age`.
- **Armazena os dados recebidos** localmente (em um arquivo de texto).
- **Resposta com "OK"** após o recebimento bem-sucedido de dados ou uma mensagem de erro se os dados forem inválidos.

### 2. Gerador de Relatório Meteorológico
- **Gera relatórios meteorológicos em PDF** com base em parâmetros de entrada, como número(s) de telefone, data e caminho para um arquivo de dados brutos.
- **Suporta formatação dinâmica de relatórios** com base em diferentes fenômenos meteorológicos.
- **Envia relatórios por e-mail** se o parâmetro `--send_email` estiver presente.
- **Registra todas as atividades** usando uma biblioteca de registro de logs `logging`.

## Tecnologias
- **Python 3.10.x**
- **Socket TCP/IP**
- **Biblioteca de geração de PDF** fpdf
- **Biblioteca nativa de e-mail** smtplib
- **Biblioteca nativa de logs** módulo `logging` do Python)

## Instruções

### Clonar Repositorio
```bash
git clone https://github.com/your-username/nimbus-python-test.git
cd nimbus-python-test
```

### Recomendação
> Para executar os próximos comandos é recomendado a criação de um ambiente virtural com o seguinte comando.
```
$ python3.10 -m venv minha_venv
```
Se estiver utilizando sistema Linux, execute o seguinte comando para ativar o ambiente virtual
```
$ source minha_venv/bin/activate
```
Após a ativação seu terminal deve fica assim:
```
(minha_venv) $
```
O ambiente virtual ajuda a isolar as dependências e evita comflitos.
### Instalação de  Dependencias

```bash
pip install -r requirements.txt
```

## Executando aplicações

### Applicação 1: Serviço Continuo de Receptação de Dados
1. **Inicie o servidor**:
   ```bash
   python data_receiver.py
   ```
   ![alt text](image.png)
   
   Isso iniciará o servidor TCP/IP na porta 5784 e o manterá em execução continuamente e pronto para receber dados.

   ## **Enviando dados para o server**:

   Para conectar e enviar dados para o servidor utilize uma ferramenta de conexão TCP/IP de sua preferência.
   Aqui estão exemplos de como utlizar.
   
   ```
   $ netcat localhost 5784
   name,email,phone,age
   Ok
   ```
   ou
   ```
   $ telnet localhost 5784
   ```
   ou
   ```
   $ curl telnet://localhost:5784
   ```


2. **Parando o servidor**:

   Execute um comando de parada explícito, como `ctrl + c`, ou encerre o processo manualmente.

### Applicação 2: Gerador de Relatório Meteorológico
1. **Gere um relatório** executando o script com os parâmetros apropriados:
   ```bash
   python report_generator.py --phone "01234567891" --date "2024-01-01T00:00" --file "bruto.txt" --send_email
   ```
   > o arquivo bruto.txt precisa estar na pasta raiz do projeto que a a pasta `nimbus-python-test`

   Esse comando gerará um relatório em PDF e o enviará por e-mail se a flag `--send_email` estiver presente.

2. **Output**:
   - O relatório em PDF será gerado e salvo na pasta reports .
   - Os logs serão salvos nos arquivos `server.log` e `generate_report.log` na pasta do projeto.

## Contato

Para quaisquer dúvidas ou problemas, entre em contato através de [amaurisantospro@gmail.com](mailto:amaurisantospro@gmail.com).

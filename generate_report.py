import os
import re
import json
import logging
import argparse
from datetime import datetime

from fpdf import FPDF

from services.email import email_service
from services.report import ReportHeader, ReportPDF

logging.basicConfig(
    filename='generate_report.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - REPORT %(message)s', 
    level=logging.INFO
)


def get_client_data(phone_numbers):
    """
    Retrieves the clients data from the .txt file that 
    was populated by the TCP/IP server. 
    Transform it into a dictionary and return it.
    """
    logging.info('Recuperando dados do cliente...')
    clients = []

    with open('data_received.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            name, email, phone_number, age = line.strip().split(',')
            if phone_number in phone_numbers:
                clients.append({
                    'name': name,
                    'email': email,
                    'phone_number': phone_number,
                    'age': age
                })
    return clients


def validate_date(date_str):
    date_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'

    if not re.match(date_regex, date_str):
        msg = 'Formato de data invalido. Formato esperado: YYYY-MM-DDTHH:MM'
        logging.info(msg)
        return False, msg

    try:
        datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        msg = 'Data ou hora invalido.'
        logging.info(msg)
        return False, msg

    return True, 'Valido.'


def get_date_hour(date_hour) -> str:
    date, hour = date_hour.split('T')
    date = date.split('-')
    date.reverse()
    return date, hour


def create_reports_dir():
    if not os.path.isdir('reports'):
        os.mkdir('reports')


def main():
    create_reports_dir()
    try:
        parser = argparse.ArgumentParser(description='Gera relatórios meteorológicos com base em parâmetros de entrada.')
        parser.add_argument('--phone', help='Telefones dos clientes separados por vírgula')
        parser.add_argument('--date', help='Data do relatório no formato YYYY-MM-DDTHH:MM')
        parser.add_argument('--file', help='Caminho para o arquivo .txt com dados de meteorologia', default='file.txt')
        parser.add_argument('--send_email', action='store_true', help='Flag para enviar o relatório por e-mail')

        logging.info('Coletando os dados passados pelo comando...')
        args = parser.parse_args()
        
        is_valid, msg = validate_date(args.date)
        
        if not is_valid:
            raise Exception(msg)

        with open(args.file, 'r') as file:
            file_data = json.load(file)
            logging.info('Acessando o arquivo bruto.txt...')

        analysis = file_data.get('análise', [])
        predictions = file_data.get('previsao', [])

        phone_numbers = args.phone.split(',')
        clients = get_client_data(phone_numbers)

        if not clients:
            msg = f'Não existe clientes com esse(s) telefone(s): {" ".join(phone_numbers)}'
            print(msg)
            logging.warning(msg)

        for client in clients:
            logging.info('Criado PDF para geração do relatório...')
            pdf = FPDF()
            report_header = ReportHeader(pdf)
            report_pdf = ReportPDF(client, pdf, report_header)
            section_list = [
                {'Análise': analysis}, 
                {'Previsão': predictions}
            ]
            logging.info('Gerando PDF do relatório...')
            pdf_file = report_pdf.generate_report_pdf(section_list)

            msg = f'Relatório gerado: {pdf_file}'
            print(msg)
            logging.info(msg)

            if args.send_email:
                date, hour = get_date_hour(args.date)
                SUBJECT = f'Relatório Meteorológico {"/".join(date)} às {hour}'
                BODY = f'Olá.\n\nSegue em anexo o relatório meteorológico do dia {"/".join(date)} às {hour}\n\nHavendo dúvidas, por favor, entre em contato.'
                logging.info('Enviando arquivo PDF do relatório via email...')
                email_service.send_email(
                    body=BODY,
                    subject=SUBJECT,
                    recipient=client['email'], 
                    attachment_path=pdf_file
                )
                msg = 'E-mail enviado com sucesso!'
                logging.info(msg)
                print(msg)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

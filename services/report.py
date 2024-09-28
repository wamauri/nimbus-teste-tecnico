from datetime import datetime

from fpdf import FPDF


class Report:
    def __init__(self, pdf: FPDF) -> None:
        self.pdf = pdf
        self.WIDTH_PDF_AREA = 210
        self.X_MARGIN = 20
        self.CELL_HEIGHT = 10
        self.INDENT_MESSAGE = '\u00A0' * 35
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GRAY = (85,85,85)

    def _get_date(self) -> str:
        return datetime.now().strftime('%d/%m/%Y')


class BuildReportHeader(Report):
    def __init__(self, pdf: FPDF) -> None:
        self.BLUE = (5,55,95)
        self.ORANGE = (255,170,60)
        super().__init__(pdf)

    def make_pdf_header(self, title: str) -> FPDF:
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.WHITE)
        self.pdf.set_fill_color(*self.BLUE)
        self.pdf.cell(
            w=self.WIDTH_PDF_AREA, 
            h=self.CELL_HEIGHT+1, 
            txt=title, 
            ln=True, 
            align='C', 
            fill=True
        )
        self.pdf.set_fill_color(*self.ORANGE)
        self.pdf.cell(self.WIDTH_PDF_AREA, 2, ln=True, fill=True)
        self.pdf.set_text_color(*self.BLACK)

        return self.pdf


class ReportClientName(Report):
    def __init__(self, pdf: FPDF, ) -> None:
        super().__init__(pdf)
    def add_client_name(self, client_name: str) -> FPDF:
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.set_margins(left=self.X_MARGIN/2, right=self.X_MARGIN/2, top=0.0)
        self.pdf.set_left_margin(self.X_MARGIN/2)
        self.pdf.cell(17, self.CELL_HEIGHT, f"Cliente:", align='L')
        self.pdf.set_font('Arial', "", 12)
        self.pdf.cell(90, self.CELL_HEIGHT, client_name.capitalize(), align='L')

        return self.pdf


class ReportDate(Report):
    def add_date(self):
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(60, self.CELL_HEIGHT, f"Data de confecção:", align='R')
        self.pdf.set_font('Arial', "", 12)
        self.pdf.cell(23, self.CELL_HEIGHT, self._get_date(), ln=True, align='R')
        self.pdf.set_top_margin(0.0)
        self.pdf.cell(self.WIDTH_PDF_AREA - self.X_MARGIN, 5, ln=True)

        return self.pdf


class ReportHeader(Report):

    def add_header(self, pdf, client_data, section):
        pdf.set_margins(left=0.0, right=0.0, top=0.0)
        pdf.add_page()
        pdf = BuildReportHeader(pdf=pdf)
        pdf = pdf.make_pdf_header(title='Relatório Meteorológico')
        pdf = ReportClientName(pdf=pdf)
        pdf = pdf.add_client_name(client_name=client_data['name'])
        pdf = ReportDate(pdf=pdf)
        pdf = pdf.add_date()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, self.CELL_HEIGHT, section, ln=True)
        pdf.set_font('Arial', '', 12)

        return pdf


class ReportPDF(Report):
    def __init__(self, client_data, pdf, report_header) -> None:
        self.report_header = report_header
        self.client_data = client_data
        super().__init__(pdf)

    def _get_pdf_file_path(self):
        date = self._get_date().replace("/", "")
        phone = self.client_data['phone_number']
        return f"reports/relatorio_meteorologico_{phone}_{date}.pdf"

    def _get_date_hour(self, section):
        date, hour = section['data'].split('T')
        date = date.split('-')
        date.reverse()
        return date, hour

    def generate_report_pdf(self, section_list):

        for section_dict in section_list:
            for section_name, sections in section_dict.items():

                self.pdf = self.report_header.add_header(
                    self.pdf, 
                    self.client_data, 
                    section_name
                )

                for section in sections:
                    date, hour = self._get_date_hour(section)

                    if self.pdf.get_y() > 240:
                        self.pdf = self.report_header.add_header(
                            self.pdf, 
                            self.client_data, 
                            section_name
                        )

                    self.pdf.set_text_color(*self.WHITE)

                    if 'mensagem' in section:
                        if 'forte' in section['mensagem'].lower():
                            self.pdf.set_fill_color(*self.RED)
                        else:
                            self.pdf.set_fill_color(*self.GRAY)

                    self.pdf.set_font('Arial', 'B', 11)

                    if 'fenomeno' in section:
                        self.pdf.cell(
                            w=50, 
                            h=6, 
                            txt=f"{section['fenomeno'].capitalize()}", 
                            border=0, 
                            ln=True, 
                            fill=True
                        )

                    self.pdf.cell(self.WIDTH_PDF_AREA - self.X_MARGIN, 3, ln=True)
                    self.pdf.set_text_color(*self.BLACK)

                    if 'data' in section:
                        self.pdf.cell(41, 5, f"{'/'.join(date)} às {hour}")
                        self.pdf.set_font('Arial', '', 11)
                        self.pdf.set_x(10)

                    if 'mensagem' in section:
                        self.pdf.multi_cell(self.WIDTH_PDF_AREA - self.X_MARGIN, 5, f"{self.INDENT_MESSAGE}{section['mensagem'].strip()}", align='J')
                        self.pdf.set_text_color(*self.BLACK)
                        self.pdf.cell(self.WIDTH_PDF_AREA - self.X_MARGIN, 6, ln=True)

        pdf_file = self._get_pdf_file_path()
        self.pdf.output(pdf_file)

        return pdf_file

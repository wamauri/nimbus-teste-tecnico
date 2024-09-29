from datetime import datetime

from fpdf import FPDF


class Report:
    def __init__(self, pdf: FPDF) -> None:
        self.pdf = pdf
        self.WIDTH_PDF_AREA = 210 - 40
        self.HEIGHT_PDF_AREA = 297 - 20
        self.HEADER_FONT_SIZE = 12
        self.X_MARGIN = 20
        self.Y_MARGIN = 10
        self.CELL_HEIGHT = 10
        self.INDENT_MESSAGE = '\u00A0' * 35
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GRAY = (85,85,85)

        self.WIDTH_BOX = 170
        self.HEIGHT_BOX = 110
        self.X_MARGIN_BOX = 20
        self.Y_MARGIN_TOP_BOX = 30
        self.Y_MARGIN_BOTTOM_BOX = 148

    def _get_date(self) -> str:
        return datetime.now().strftime('%d/%m/%Y')


class BuildReportHeader(Report):
    def __init__(self, pdf: FPDF) -> None:
        self.BLUE = (5,55,95)
        self.ORANGE = (255,170,60)
        super().__init__(pdf)

    def make_pdf_header(self, title, x_margin_box, y_margin_box, width_box) -> FPDF:
        self.pdf.set_xy(x_margin_box, y_margin_box)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_text_color(*self.WHITE)
        self.pdf.set_fill_color(*self.BLUE)
        self.pdf.cell(
            w=width_box, 
            h=self.CELL_HEIGHT + 1, 
            txt=title, 
            ln=True, 
            align='C', 
            fill=True
        )
        self.pdf.set_xy(x_margin_box, y_margin_box+11)
        self.pdf.set_fill_color(*self.ORANGE)
        self.pdf.cell(width_box, 2, ln=True, fill=True)
        self.pdf.set_text_color(*self.BLACK)

        return self.pdf


class ReportClientName(Report):
    def __init__(self, pdf: FPDF, ) -> None:
        super().__init__(pdf)

    def add_client_name(self, client_name, x_margin_box, client_section_y) -> FPDF:
        self.pdf.set_xy(x_margin_box, client_section_y)
        self.pdf.set_font('Arial', 'B', self.HEADER_FONT_SIZE)
        self.pdf.cell(17, self.CELL_HEIGHT, f"Cliente:", align='L')
        self.pdf.set_font('Arial', "", self.HEADER_FONT_SIZE)
        self.pdf.cell(80, self.CELL_HEIGHT, client_name.capitalize(), align='L')

        return self.pdf


class ReportDate(Report):
    def add_date(self):
        self.pdf.set_font('Arial', 'B', self.HEADER_FONT_SIZE)
        self.pdf.cell(40, self.CELL_HEIGHT, f"Data de confecção:", align='R')
        self.pdf.set_font('Arial', "", self.HEADER_FONT_SIZE)
        self.pdf.cell(23, self.CELL_HEIGHT, self._get_date(), ln=True, align='R')

        return self.pdf


class ReportHeader(Report):

    def add_header(self, x_margin_box, y_margin_box, width_box, client_data, section):
        
        pdf = BuildReportHeader(pdf=self.pdf)
        pdf = pdf.make_pdf_header(
            'Relatório Meteorológico', 
            x_margin_box, 
            y_margin_box, 
            width_box
        )
        
        client_section_y = y_margin_box + self.CELL_HEIGHT + 2
        pdf = ReportClientName(pdf=self.pdf)
        pdf = pdf.add_client_name(
            client_name=client_data['name'], 
            x_margin_box=x_margin_box + 5, 
            client_section_y=client_section_y
        )

        pdf = ReportDate(pdf=self.pdf)
        pdf = pdf.add_date()
        
        self.pdf.set_xy(x_margin_box + 5, client_section_y + 9)
        self.pdf.set_font('Arial', 'B', self.HEADER_FONT_SIZE)
        self.pdf.cell(100, self.CELL_HEIGHT, section, ln=True)
        self.pdf.set_font('Arial', '', 12)
        pdf.set_left_margin(x_margin_box + 5)

        return self.pdf


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

    def draw_box(self, y_box):
        self.pdf.set_xy(
            self.X_MARGIN_BOX, 
            y_box
        )
        self.pdf.rect(
            self.X_MARGIN_BOX, 
            y_box, 
            self.WIDTH_BOX, 
            self.HEIGHT_BOX
        )

    def message_height(self, msg, box_width):
        """
        Method for calculating the required height for a message, 
        without actually printing it to the PDF.
        """
        return self.pdf.get_string_width(msg) / box_width * self.CELL_HEIGHT

    def can_fit_message(self, msg, current_y_position, box_start_y, box_height, box_width):
        """
        Checks whether the message fits in the 
        available space on the board.
        """
        message_height = self.message_height(msg, box_width)
        available_space = box_start_y + box_height - current_y_position

        return message_height <= available_space

    def add_content_to_pdf(self, item):
        self.pdf.set_text_color(*self.WHITE)

        if 'mensagem' in item:
            if 'forte' in item['mensagem'].lower():
                self.pdf.set_fill_color(*self.RED)
            else:
                self.pdf.set_fill_color(*self.GRAY)

        self.pdf.set_font('Arial', 'B', 9)

        if 'fenomeno' in item:
            self.pdf.cell(
                w=37, 
                h=5, 
                txt=f"{item['fenomeno'].capitalize()}", 
                border=0, 
                ln=True, 
                fill=True
            )

        self.pdf.set_text_color(*self.BLACK)
        date, hour = self._get_date_hour(item)

        if 'data' in item:
            self.pdf.cell(10, 1, ln=True)
            self.pdf.cell(41, 4, f"{'/'.join(date)} às {hour}")
            self.pdf.set_font('Arial', '', 9)
            self.pdf.set_x(self.X_MARGIN_BOX)

        if 'mensagem' in item:
            self.pdf.set_left_margin(self.X_MARGIN_BOX + 5)
            self.pdf.multi_cell(
                w=self.WIDTH_BOX - self.X_MARGIN_BOX / 2, 
                h=4, 
                txt=f"{self.INDENT_MESSAGE}{item['mensagem'].strip()}", 
                align='J'
            )
            self.pdf.set_text_color(*self.BLACK)
            self.pdf.cell(self.WIDTH_BOX - self.X_MARGIN_BOX / 2, 4, ln=True)

            return  self.pdf.get_y()

    def generate_report_pdf(self, section_list):

        for section_dict in section_list:

            for section_name, section_items in section_dict.items():
                current_y_position = self.Y_MARGIN_TOP_BOX + 30
                self.pdf.add_page()
                self.draw_box(self.Y_MARGIN_TOP_BOX)
                self.draw_box(self.Y_MARGIN_BOTTOM_BOX)
                
                self.pdf = self.report_header.add_header(
                    x_margin_box=self.X_MARGIN_BOX, 
                    y_margin_box=self.Y_MARGIN_TOP_BOX, 
                    width_box=self.WIDTH_BOX, 
                    client_data=self.client_data, 
                    section=section_name
                )
                self.pdf = self.report_header.add_header(
                    x_margin_box=self.X_MARGIN_BOX, 
                    y_margin_box=self.Y_MARGIN_BOTTOM_BOX, 
                    width_box=self.WIDTH_BOX, 
                    client_data=self.client_data, 
                    section=section_name
                )

                y_margin_box = self.Y_MARGIN_TOP_BOX
                items_quantity = len(section_items)
                loop = 1

                for item in section_items:
                    message = item.get('mensagem', '')
                    message_fit = self.can_fit_message(
                        message, 
                        current_y_position, 
                        y_margin_box + 20, 
                        self.HEIGHT_BOX, 
                        self.WIDTH_BOX
                    )

                    if not message_fit:
                        if not message_fit and current_y_position == 256:
                            self.pdf.add_page()
                            self.draw_box(self.Y_MARGIN_TOP_BOX)
                            self.pdf = self.report_header.add_header(
                                x_margin_box=self.X_MARGIN_BOX, 
                                y_margin_box=self.Y_MARGIN_TOP_BOX, 
                                width_box=self.WIDTH_BOX, 
                                client_data=self.client_data, 
                                section=section_name
                            )

                            if not loop == items_quantity:
                                self.draw_box(self.Y_MARGIN_BOTTOM_BOX)
                                self.pdf = self.report_header.add_header(
                                    x_margin_box=self.X_MARGIN_BOX, 
                                    y_margin_box=self.Y_MARGIN_BOTTOM_BOX, 
                                    width_box=self.WIDTH_BOX, 
                                    client_data=self.client_data, 
                                    section=section_name
                                )
                            y_margin_box = self.Y_MARGIN_TOP_BOX
                            current_y_position = self.Y_MARGIN_TOP_BOX + 30
                            self.pdf.set_xy(self.X_MARGIN_BOX + 5, current_y_position)
                            current_y_position = self.add_content_to_pdf(item)
                        else:
                            y_margin_box = self.Y_MARGIN_BOTTOM_BOX
                            current_y_position = self.Y_MARGIN_BOTTOM_BOX + 30
                            self.pdf.set_xy(self.X_MARGIN_BOX + 5, current_y_position)
                            current_y_position = self.add_content_to_pdf(item)

                    else:
                        self.pdf.set_xy(self.X_MARGIN_BOX + 5, current_y_position)
                        current_y_position = self.add_content_to_pdf(item)

                    loop += 1

        pdf_file = self._get_pdf_file_path()
        self.pdf.output(pdf_file)

        return pdf_file

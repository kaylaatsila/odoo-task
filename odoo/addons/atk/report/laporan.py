from odoo import models, fields, api
import base64
import xlsxwriter
from io import BytesIO as StringIO
from datetime import datetime
import pytz

class Laporan(models.TransientModel):
    _name = 'laporan'

    state = fields.Selection([('draft', 'Draft'),
                              ('sent', 'Requested'),
                              ('reject', 'Rejected'),
                              ('approve', 'Approved')], string='State', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    time = datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%H-%M-%S')

    name = fields.Char('File Name')
    file = fields.Binary('File', readonly=True)
    wbf = {}

    @api.multi
    def add_workbook_format(self, workbook):
        self.wbf['company'] = workbook.add_format({'bold': 1,
                                                   'align': 'left',
                                                   'font_color': 'black',
                                                   'num_format': 'dd/mm/yyyy'})
        self.wbf['company'].set_font_size(9.5)
        self.wbf['company'].set_font_name('Work Sans')

        self.wbf['company_center'] = workbook.add_format({'bold': 1,
                                                          'align': 'center',
                                                          'font_color': 'black'})
        self.wbf['company_center'].set_font_size(10)
        self.wbf['company_center'].set_font_name('Work Sans')

        self.wbf['footer'] = workbook.add_format({'align': 'left'})
        self.wbf['footer'].set_font_name('Work Sans')

        self.wbf['header'] = workbook.add_format({'bold': 1,
                                                  'align': 'center',
                                                  'font_color': 'black',
                                                  'bg_color': '#BACDDB'})
        self.wbf['header'].set_top()
        self.wbf['header'].set_bottom()
        self.wbf['header'].set_left()
        self.wbf['header'].set_right()
        self.wbf['header'].set_font_size(9)
        self.wbf['header'].set_align('vcenter')
        self.wbf['header'].set_font_name('Work Sans')

        self.wbf['header_left'] = workbook.add_format({'bold': 1,
                                                       'align': 'center',
                                                       'font_color': 'black',
                                                       'bg_color': '#BACDDB'})
        self.wbf['header_left'].set_top()
        self.wbf['header_left'].set_bottom()
        self.wbf['header_left'].set_left()
        self.wbf['header_left'].set_right()
        self.wbf['header_left'].set_font_size(9)
        self.wbf['header_left'].set_font_name('Work Sans')
        self.wbf['header_left'].set_align('vcenter')

        self.wbf['header_right'] = workbook.add_format({'bold': 1,
                                                        'align': 'center',
                                                        'font_color': 'black',
                                                        'bg_color': '#BACDDB'})
        self.wbf['header_right'].set_top()
        self.wbf['header_right'].set_bottom()
        self.wbf['header_right'].set_left()
        self.wbf['header_right'].set_right()
        self.wbf['header_right'].set_font_size(9)
        self.wbf['header_right'].set_font_name('Work Sans')
        self.wbf['header_right'].set_align('vcenter')

        self.wbf['content'] = workbook.add_format({'align': 'left',
                                                   'font_color': 'black'})
        self.wbf['content'].set_left()
        self.wbf['content'].set_right()
        self.wbf['content'].set_top()
        self.wbf['content'].set_bottom()
        self.wbf['content'].set_font_size(9)
        self.wbf['content'].set_font_name('Work Sans')

        self.wbf['content_center'] = workbook.add_format({'align': 'center',
                                                          'font_color': 'black'})
        self.wbf['content_center'].set_left()
        self.wbf['content_center'].set_right()
        self.wbf['content_center'].set_top()
        self.wbf['content_center'].set_bottom()
        self.wbf['content_center'].set_font_size(9)
        self.wbf['content_center'].set_font_name('Work Sans')

        self.wbf['content_right'] = workbook.add_format({'align': 'right',
                                                         'font_color': 'black'})
        self.wbf['content_right'].set_left()
        self.wbf['content_right'].set_right()
        self.wbf['content_right'].set_top()
        self.wbf['content_right'].set_bottom()
        self.wbf['content_right'].set_font_size(9)
        self.wbf['content_right'].set_font_name('Work Sans')

        self.wbf['content_right_bold'] = workbook.add_format({'bold': 1,
                                                              'align': 'right',
                                                              'font_color': 'black'})
        self.wbf['content_right_bold'].set_left()
        self.wbf['content_right_bold'].set_right()
        self.wbf['content_right_bold'].set_top()
        self.wbf['content_right_bold'].set_bottom()
        self.wbf['content_right_bold'].set_font_size(9)
        self.wbf['content_right_bold'].set_font_name('Work Sans')

        self.wbf['content_curr'] = workbook.add_format({'align': 'right',
                                                        'font_color': 'black'})
        self.wbf['content_curr'].set_left()
        self.wbf['content_curr'].set_right()
        self.wbf['content_curr'].set_top()
        self.wbf['content_curr'].set_bottom()
        self.wbf['content_curr'].set_font_size(9)
        self.wbf['content_curr'].set_font_name('Work Sans')
        self.wbf['content_curr'].set_num_format(8)

        self.wbf['content_curr_bold'] = workbook.add_format({'bold': 1,
                                                             'align': 'right',
                                                             'font_color': 'black'})
        self.wbf['content_curr_bold'].set_left()
        self.wbf['content_curr_bold'].set_right()
        self.wbf['content_curr_bold'].set_top()
        self.wbf['content_curr_bold'].set_bottom()
        self.wbf['content_curr_bold'].set_font_size(9)
        self.wbf['content_curr_bold'].set_font_name('Work Sans')
        self.wbf['content_curr_bold'].set_num_format(8)

        return workbook

    @api.multi
    def generate_report(self):
        fp = StringIO()
        workbook = xlsxwriter.Workbook(fp)
        workbook = self.add_workbook_format(workbook)
        wbf = self.wbf
        worksheet = workbook.add_worksheet('Laporan Transaksi')

        worksheet.set_column('B1:B1', 4)
        worksheet.set_column('C1:C1', 20)
        worksheet.set_column('D1:D1', 20)
        worksheet.set_column('E1:E1', 20)
        worksheet.set_column('F1:F1', 20)
        worksheet.set_column('G1:G1', 20)

        query = ("""
								select d.division_name, m.product_name, m.product_price, p.quantity
								from produk m, divisi d, produk_transaksi p, transaksi t
								where m.id = p.product and (t.id = p.transaction 
													  					 and d.id = t.division
                                			 and t.state = '%s' 
                                			 and (t.date between '%s' and '%s'))
                """) % (str(self.state),
                        str(self.start_date),
                        str(self.end_date))

        self.env.cr.execute(query)

        ress = self.env.cr.fetchall()

        worksheet.merge_range('B1:G1',
                              'Laporan Transaksi ATK',
                              wbf['company_center'])
        worksheet.merge_range('B2:G2',
                              ('Tanggal : %s s.d. %s') % (str(self.start_date),
                                                          str(self.end_date)),
                              wbf['company'])
        worksheet.merge_range('B3:G3',
                              ('Status : %s') % str(self.state),
                              wbf['company'])

        row = 4
        worksheet.write(('B%s') % (row+1), 'No', wbf['header_left'])
        worksheet.write(('C%s') % (row+1), 'Divisi', wbf['header_left'])
        worksheet.write(('D%s') % (row+1), 'Nama Produk', wbf['header'])
        worksheet.write(('E%s') % (row+1), 'Harga Satuan', wbf['header'])
        worksheet.write(('F%s') % (row+1), 'Jumlah Pembelian', wbf['header'])
        worksheet.write(('G%s') % (row+1), 'Sub Total', wbf['header_right'])
        row += 2

        if ress == []:
            worksheet.merge_range(('B%s:G%s') % (row, row),
                                  'Data tidak ada!',
                                  wbf['content'])
        no = 1
        for res in ress:
            worksheet.write(('B%s') % (row), no, wbf['content_center'])
            worksheet.write(('C%s') % (row), res[0], wbf['content'])
            worksheet.write(('D%s') % (row), res[1], wbf['content'])
            worksheet.write(('E%s') % (row), res[2], wbf['content_curr'])
            worksheet.write(('F%s') % (row), res[3], wbf['content_right'])
            worksheet.write(('G%s') % (row),
                            ('=E%s * F%s') % ((row), (row)),
                            wbf['content_curr'])
            row += 1
            no += 1

        worksheet.merge_range(('B%s:F%s') % (row, row),
                              'Grand Total',
                              wbf['content_curr_bold'])
        worksheet.write(('G%s') % (row),
                        ('=SUM(G5:G%s)') % (row-1),
                        wbf['content_curr_bold'])
        workbook.close()

        out = base64.encodestring(fp.getvalue())

        self.write({'file': out,
                    'name': ('%s_Report_%s_%s.xlsx') % ((str(self.state)).title(),
                                                        str(self.start_date),
                                                        str(self.time))})

        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'url': ('/web/content/laporan/%s/file/%s?download=true') % (self.id, self.name),
            'name': 'contract', }

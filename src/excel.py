import xlwt

class Export:
    @classmethod
    def Excel(cls, msnv, hotennv, list_day, list_gio, file_name):
        book = xlwt.Workbook(encoding="utf-8")
        sh = book.add_sheet("sheet 1", cell_overwrite_ok=True)

        col1_name = 'Mã số NV'
        col2_name = 'Họ và Tên'
        col3_name = 'Ngày điểm danh'
        col4_name = 'Giờ'
        n=0
        sh.write(0, 0, col1_name)
        sh.write(0, 2, col2_name)
        sh.write(0, 4, col3_name)
        sh.write(0, 6, col4_name)

        for m, e1 in enumerate(msnv, n+1):
            sh.write(m, 0, e1)

        for m, e2 in enumerate(hotennv, n+1):
            sh.write(m, 2, e2)

        for m, e3 in enumerate(list_day, n+1):
            sh.write(m, 4, e3)

        for m, e4 in enumerate(list_gio, n+1):
            sh.write(m, 6, e4)

        return book.save(file_name)

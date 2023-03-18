import xlwt

class Export:
    @classmethod
    def excel(cls, numberIds, names, dateList, timeList, fileName):
        book = xlwt.Workbook(encoding = 'utf-8')
        sheetAddRow = book.add_sheet('result attendance', cell_overwrite_ok = True)

        columnNumberId = 'number Id'
        columnName = 'name'
        columnDate = 'date attendance'
        columnTime = 'time attendance'
        n = 0
        sheetAddRow.write(0, 0, columnNumberId)
        sheetAddRow.write(0, 2, columnName)
        sheetAddRow.write(0, 4, columnDate)
        sheetAddRow.write(0, 6, columnTime)

        for m, e1 in enumerate(numberIds, n + 1):
            sheetAddRow.write(m, 0, e1)

        for m, e2 in enumerate(names, n + 1):
            sheetAddRow.write(m, 2, e2)

        for m, e3 in enumerate(dateList, n + 1):
            sheetAddRow.write(m, 4, e3)

        for m, e4 in enumerate(timeList, n + 1):
            sheetAddRow.write(m, 6, e4)

        return book.save(fileName)

from wtforms import DateField, TimeField


def _campo_de_data_e_de_tempo_process_formdata(self, valuelist):
    if isinstance(valuelist[0], str):
        self.data = valuelist[0]
        return
    else:
        self.data = None
        return


class DateFieldSemValidacaoFormato(DateField):
    def process_formdata(self, valuelist):
        return _campo_de_data_e_de_tempo_process_formdata(self, valuelist)


class TimeFieldSemValidacaoFormato(TimeField):
    def process_formdata(self, valuelist):
        return _campo_de_data_e_de_tempo_process_formdata(self, valuelist)

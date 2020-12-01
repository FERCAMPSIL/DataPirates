from functools import partial
from ..items import GravaItemLoader, UfItemLoader
from .constantes import *
from scrapy.http import FormRequest
from scrapy import Spider
from scrapy.selector import Selector



class CorreiosSpider(Spider):

    name = 'correios'
    start_urls = [
        'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm'
    ]
    created_ufs = {}
    #
    def parse(self, response):
        for uf_option_value in response.xpath("//select[@class='f1col']/option/@value"):
            uf_selected = uf_option_value.get()
            if not self.is_uf_table(uf_selected):

                formdata = {DATA_UF: uf_selected}
                self.set_ufitemloader(response, uf_selected)

                yield FormRequest.from_response(response,
                                                formname=NAME_GERAL,
                                                formdata=formdata,
                                                callback=partial(self.parse_result,uf_selected=uf_selected))
    #CASO A OPTION DE UF SEJA VAZIA 
    def is_uf_table(self, uf_selected):
        return uf_selected is ''

    def set_ufitemloader(self, response, uf_selected):
        if uf_selected not in self.created_ufs.keys():
            ufloader = UfItemLoader(selector=Selector(response))
            ufloader.add_value(ITEM_FIELD_UF, uf_selected)
            self.created_ufs[uf_selected] = ufloader

    def parse_result(self, response, uf_selected):
        result_tables = response.xpath(".//table[@class='tmptabela']")

        table_content = self.get_table_content(result_tables)

        grava_loader = GravaItemLoader(selector=Selector(response))
        for td_index in range(len(table_content.xpath(".//tr/td").getall())):
            self.set_grava_loader(grava_loader, table_content, td_index)

        formdata = {DATA_UF: uf_selected, DATA_LOCALIDADE: DATA_ALL_VALUES}

        self.set_grava_item(grava_loader, uf_selected)

        yield from self.yield_result(formdata, response, uf_selected)

    def yield_result(self, formdata, response, uf_selected):
        next_page_form = response.xpath("//form[@name=" + NAME_PROXIMA + "]").get()

        if next_page_form is not None:
            yield FormRequest.from_response(response,
                                            formname=NAME_PROXIMA,
                                            formdata=formdata,
                                            callback=partial(self.parse_result, uf_selected=uf_selected))
        else:
            uf_item = self.created_ufs[uf_selected].load_item()
            yield uf_item

    def set_grava_item(self, grava_loader, uf_selected):
        uf_item = self.created_ufs[uf_selected].load_item()
        grava_item = grava_loader.load_item()

        if uf_item.get(ITEM_FIELD_GRAVA) is None:
            uf_item[ITEM_FIELD_GRAVA] = grava_item
        else:
            uf_item[ITEM_FIELD_GRAVA][ITEM_FIELD_LOCALIDADE].extend(grava_item[ITEM_FIELD_LOCALIDADE])
            uf_item[ITEM_FIELD_CEP][ITEM_FIELD_CEP].extend(grava_item[ITEM_FIELD_CEP])

    def get_table_content(self, result_tables):
        table_content = result_tables[0]
        if len(result_tables) > 1:
            table_content = result_tables[1]
        return table_content

    def set_grava_loader(self, grava_loader, table_content, td_index):
        total_columns = 4
        localidade_index = 0
        cep_index = 1
        
        column_content = table_content.xpath(".//tr/td").getall()[td_index]
        if (td_index % total_columns) == localidade_index:
            grava_loader.add_value(ITEM_FIELD_LOCALIDADE, column_content)
        elif (td_index % total_columns) == cep_index:
            grava_loader.add_value(ITEM_FIELD_CEP, column_content)
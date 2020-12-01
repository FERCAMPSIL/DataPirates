from scrapy.utils.markup import remove_tags
from scrapy.loader.processors import TakeFirst, MapCompose, Compose
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader


#Classes para preencher e gravar  os items 

#grava item removendo tags da tabela em html, usando lambda para remover os espaços na string
class GravaItem(Item):
    localidade = Field(input_processor=MapCompose(remove_tags))
    faixa_de_cep = Field(input_processor=MapCompose(remove_tags, lambda string: string.strip()))


class UfItem(Item):
    uf = Field()
    grava = Field(serializer=GravaItem)

class GravaItemLoader(ItemLoader):
    default_item_class = GravaItem
    default_output_processor = Compose()


class UfItemLoader(ItemLoader):
    default_item_class = UfItem
    default_output_processor = TakeFirst()




Esta foi a minha solução encontrada para este desafio  

### Requisitos:

 ** Criar ** ambiente virtual, estou usando uma  [virtualenv], com o nome correios (https://virtualenv.pypa.io/en/latest/). Para executar o projeto, você precisará de:
* [Python] (https://www.python.org/) 3+
* [Scrapy] (https://scrapy.org/) 1.7.2

 Instalar as libs acima usando [pip] (https://pypi.org/project/pip/).Vá para a ** pasta raiz ** e execute `pip install -r requirements.txt`.


### Execução:
 Vá para a pasta raiz' e execute o `scrapy crawl correios -o data / data.json`, isso irá retirar os dados do site [correios] (http://www.buscacep.correios.com .br/sistemas/buscacep/buscaFaixaCEP.cfm) salvando na pasta de dados_ para uma análise de dados 



#### Observações 
Um `registro` pode conter várias cidades, portanto` localidade` 'n `faixa_de_cep` são ambos arrays onde seus índices têm um mapeamento um-para-um' (por exemplo,` localidade [2] `estar diretamente relacionado com '` faixa_de_cep [2] `).
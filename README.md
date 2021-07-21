# API CriptoFácil

Esta aplicação irá fazer a consolidação de investimentos em criptomoedas facilitando o controle de da rentabilidade de suas posições e realizando os cálculos necessários para as obrigações tributárias.

# Endpoints

## User

Este endpoint possui duas rotas: uma rota para cadastro de usuários e uma rota para o login de usuários. 

### Point Request

Rota para **cadastro** de um novo usuário.

```markdown
POST https://criptofacil-deploy.herokuapp.com/api/register
```

### JSON Content

```json
{
	"name": "<nome>",
	"last_name": "<sobrenome>",
	"email": "<nome@mail.com>",
	"password": "<senha>"
}
```

### Response Format

```json
{
	"id": "<id>"
	"name": "<nome>",
	"last_name": "<sobrenome>",
	"email": "<nome@mail.com>"
}
```

### Point Request

Rota para login de um usuário cadastrado.

```markdown
POST https://criptofacil-deploy.herokuapp.com/api/login
```

### JSON Content

```json
{
	"email": "<nome@mail.com>",
	"password": "<senha>"
}
```

### Response Format

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzIaCI6ZmFsc2UsImlhdCI6MTYyNjcwNDQ2MCwianRpIjoiOTQ4YmY2YjUtYWI4Mi00NDNlLWFiOWUtZDBlNGYxZjRhYWI4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNjI2NzA0NDYwLCJleHAiOjE2MjczMDkyNjB9.0trKMIZFPHJUC0FXdmuhwTlI87jJiIrT16zLAlzfj2M"
}
```

## Transactions

Este endpoint terá informações referentes as transações do usuário. O usuário poderá registrar uma nova transação, verificar o histórico de todas as transações e o histórico filtrado por moeda, editar e excluir uma transação. 

### Point Request

Rota para registrar uma transação.

```markdown
POST https://criptofacil-deploy.herokuapp.com/api/transactions/register
```

### JSON Content

Os campos do JSON devem ser preenchidos da seguinte forma:

- **"date"** deve ser preenchido no formato YYYY-MM-DD;
- **"type"** é referente ao tipo de transação e pode ser do tipo "buy", indicando uma compra, "sell", indicando uma venda, "input" indicando uma criptomoeda utilizada para permuta por outra criptomoeda, e "input", indicando a criptomoeda comprada na permuta;
- **"coin"** deve ser preenchido com a moeda que será transacionada. A moeda deve estar contida na lista de moedas a seguir: 'bitcoin', 'ethereum', 'tether', 'cardano', 'litecoin', 'stellar', 'usd-coin', 'eos', 'monero', 'binance-usd', 'tezos', 'neo', 'nem', 'zilliqa', 'icon', 'true-usd', 'dash' e 'decred';
- **"fiat"** é referente a moeda fiduciária usado como referência no preço indicado no campo "price_per_coin";
- **"price_per_coin"** é referente ao preço de compra ou venda da cripomoeda transacionada;
- **"quantity"** é referente quantidade da cripomoeda transacionada;
- **"foreign_exch"** indica o país onde a transação foi realizada. Em caso de transação em exchange no exterior, o valor deve ser "true", transação em exchange brasileira deve ter o valor "false".

```json
{
    "date": "2021-05-06",
    "type": "<buy>",
    "coin": "<bitcoin>",
    "fiat": "<brl>",
    "price_per_coin": 25,
    "quantity": 100,
    "foreign_exch": true
}
```

### Response Format

A resposta será em formato JSON e trará os seguintes campos adicionais na resposta:

- **"avg_price_brl"** referente ao preço médio ponderado em BRL das transações de compra até a data do registro;
- **"avg_price_usd"** referente ao preço médio ponderado em USD das transações de compra até a data do registro;
- **"net_quantity"** referente a quantidade líquida da moeda em questão até a data do registro.

```json
{
  "id": 53,
  "date": "Thu, 06 May 2021 00:00:00 GMT",
  "type": "buy",
  "coin": "bitcoin",
  "fiat": "brl",
  "price_per_coin": 25,
  "avg_price_brl": 25,
  "avg_price_usd": 4.726165945138666,
  "net_quantity": 100,
  "quantity": 100,
  "foreign_exch": true
}
```

### Point Request

Rota para verificar o histórico de todas as transações.

```markdown
GET https://criptofacil-deploy.herokuapp.com/api/transactions
```

### Response Format

A resposta será em formato JSON e trará os seguintes campos adicionais na resposta:

- **"ptax"** referente a cotação de venda informada pelo Banco Central no dia da transação;

```json
[	
	{
	  "bitcoin": [
	    {
	      "id": 47,
	      "date": "Thu, 06 May 2021 00:00:00 GMT",
	      "type": "buy",
	      "coin": "bitcoin",
	      "fiat": "brl",
	      "price_per_coin": 25,
	      "quantity": 50,
	      "net_quantity": 50,
	      "avg_price_brl": 25,
	      "avg_price_usd": 4.73,
	      "foreign_exch": true,
	      "ptax": 5.2897
	    },
	  ],
	  "litecoin": [
	    {
	      "id": 49,
	      "date": "Thu, 06 May 2021 00:00:00 GMT",
	      "type": "buy",
	      "coin": "litecoin",
	      "fiat": "brl",
	      "price_per_coin": 25,
	      "quantity": 200,
	      "net_quantity": 200,
	      "avg_price_brl": 25,
	      "avg_price_usd": 4.73,
	      "foreign_exch": true,
	      "ptax": 5.2897
	    }	
	  ]
	}
]
```

### Point Request

Rota para verificar o histórico de todas as transações filtrado por moeda.

```markdown
GET https://criptofacil-deploy.herokuapp.com/api/transactions/<coin>
```

### Response Format

```json
[
	{
	  "bitcoin": [
	    {
	      "id": 47,
	      "date": "Thu, 06 May 2021 00:00:00 GMT",
	      "type": "buy",
	      "coin": "bitcoin",
	      "fiat": "brl",
	      "price_per_coin": 25,
	      "quantity": 50,
	      "net_quantity": 50,
	      "avg_price_brl": 25,
	      "avg_price_usd": 4.73,
	      "foreign_exch": true,
	      "ptax": 5.2897
	    },
	    {
	      "id": 48,
	      "date": "Thu, 06 May 2021 00:00:00 GMT",
	      "type": "buy",
	      "coin": "bitcoin",
	      "fiat": "brl",
	      "price_per_coin": 25,
	      "quantity": 100,
	      "net_quantity": 150,
	      "avg_price_brl": 25,
	      "avg_price_usd": 4.73,
	      "foreign_exch": true,
	      "ptax": 5.2897
	    }
	  ]
	}
]
```

### Point Request

Rota para editar uma transação.

```markdown
PUT https://criptofacil-deploy.herokuapp.com/api/transactions/<id>
```

### JSON Content

```json
{
    "date": "2021-01-06",
    "type": "buy",
    "coin": "litecoin",
    "fiat": "brl",
    "price_per_coin": 20,
    "net_quantity": 10,
    "quantity": 10,
    "foreign_exch": true
}
```

### Response Format

```json
{
  "id": 52,
  "date": "Wed, 06 Jan 2021 00:00:00 GMT",
  "type": "buy",
  "coin": "litecoin",
  "fiat": "brl",
  "price_per_coin": 20,
  "avg_price_brl": 25,
  "avg_price_usd": 4.726165945138666,
  "net_quantity": 10,
  "quantity": 10,
  "foreign_exch": true
}
```

### Point Request

Rota para deletar uma transação.

```markdown
DELETE https://criptofacil-deploy.herokuapp.com/api/transactions/<id>
```

### Response Format

```json
{}
```

## Portfolio

Este endpoint irá retornar  um JSON com a informações referentes a posição do usuário em cada moeda. tais como: preço médio das compras, quantidade atual, preço da moeda no momento, variação de preço da moeda nas últimas 24 horas, posição total no momento e o valor de lucro ou prejuízo no momento. Todos os valores estão na moeda BRL.

### Point Request

```markdown
GET https://criptofacil-deploy.herokuapp.com/api/portfolio/list
```

### Response Format

```json
[
  {
    "coin": "bitcoin",
    "avg_price": 190000.0,
    "quantity": 0.1,
    "current_price": 164581,
    "24h_change": 5.31,
    "current_position": 16458.1,
    "profit": -2541.9
  },
  {
    "coin": "ethereum",
    "avg_price": 11000.0,
    "quantity": 0.5,
    "current_price": 10104.27,
    "24h_change": 7.22,
    "current_position": 5052.14,
    "profit": -447.86
  }
]
```

## Accounting

## Chart

Este endpoint irá retornar  um JSON com as informações necessárias para gerar um gráfico da evolução patrimonial do usuário. As chaves do JSON são os meses do ano até o mês vigente e os valores são o produto entre o preço da moeda e a quantidade em carteira no último dia de cada mês. O valor do mês vigente utiliza a cotação da moeda no momento da geração dos dados.

### Point Request

```markdown
GET https://criptofacil-deploy.herokuapp.com/api/chart
```

### Response Format

```json
{
  "jan": 1868.08,
  "fev": 2612.22,
  "mar": 3387.23,
  "abr": 2860.94,
  "mai": 3733.19,
  "jun": 3565.82,
  "jul": 3295.02
}
```

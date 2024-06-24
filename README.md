# Projeto: Data Logger com InfluxDB e Docker

Este projeto é um Data Logger que gera dados aleatórios e os envia para um banco de dados InfluxDB em intervalos regulares. O projeto é containerizado usando Docker para facilitar a implantação e execução.

## Funcionalidades

- Geração de dados aleatórios.
- Registro de logs detalhados usando a biblioteca `logging`.
- Envio dos dados gerados para um banco de dados InfluxDB.
- Uso do `schedule` para executar a tarefa de geração e envio de dados em intervalos regulares.
- Dockerfile para criação de um contêiner Docker que executa o script Python.

## Pré-requisitos

- Docker instalado na máquina.
- Conta no InfluxDB Cloud ou uma instância do InfluxDB rodando localmente.

## Configuração

### InfluxDB

1. Crie um bucket no InfluxDB.
2. Gere um token de acesso.
3. Anote o nome da sua organização.

### Variáveis de Configuração

Edite as seguintes variáveis no script `script.py`:

```python
url = "http://localhost:8086"  # Coloque seu endereço do InfluxDB
token = ""  # Substitua pelo seu token gerado
org = ""  # Substitua pelo nome da sua organização
bucket = ""  # Substitua pelo nome do seu bucket
```

## Estrutura do Projeto

- `script.py`: Contém o script principal que gera dados aleatórios e os envia para o InfluxDB.
- `Dockerfile`: Arquivo de configuração para criar a imagem Docker.

## Como Executar

### Localmente

1. Instale as dependências:

   ```sh
   pip install influxdb_client schedule
   ```

2. Execute o script:

   ```sh
   python script.py
   ```

### Usando Docker

1. Construa a imagem Docker:

   ```sh
   docker build -t data-logger .
   ```

2. Execute o contêiner:

   ```sh
   docker run -d --name data-logger --restart always --network="host" data-logger
   ```

## Logs

Os logs são salvos no arquivo `py.log` e também exibidos no console. O logger é configurado para registrar mensagens de diferentes níveis, incluindo debug, info, warning, error e critical.

## Código Principal

```python
import influxdb_client
import random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time
import schedule
import logging

# Configurar o nível de registro
logging.basicConfig(filename='BOT.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        encoding='utf-8',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

# Criar um logger
logger = logging.getLogger("docker-pyhon")

# Definir um formato para as mensagens de registro
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Criar um manipulador de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Adicionar o manipulador ao logger
logger.addHandler(console_handler)

logger.info("Iniciando tarefa....")

# Configuração do InfluxDB
url = "http://localhost:8086" #coloque seu endereço
token = ""  # Substitua por seu token gerado
org = ""  # Substitua pelo nome da sua organização
bucket = "" #coloque eu bucket

write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def write_random_data():
    try:
        for i in range(10):
            value = random.uniform(0, 100)
            tag_value = random.choice(['tag1', 'tag2', 'tag3'])
            logger.info(f'random {value} random tag {tag_value}')

            point = Point("random_measurement") \
                .tag("tagname", tag_value) \
                .field("value", value) \
                .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket=bucket, org=org, record=point)
            print(f'Written: {value} with tag {tag_value}')
            logger.info(f"escrevendo valor:{value} tag:{tag_value}")
            time.sleep(1)

    except Exception as e:
        print(f"Erro ao escrever dados aleatórios: {e}")
        logger.error(f"erro:{e}")

schedule.every(1).minutes.do(write_random_data)
logger.info('rodei!!')

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install influxdb_client schedule

COPY script.py .

CMD ["python", "script.py"]
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Contato

E-mail:falecomjuliasantana@gmail.com

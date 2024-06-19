import influxdb_client
import random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time
import schedule
import logging

# Configurar o nível de registro
logging.basicConfig(filename='py.log',
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

    # Exemplos de mensagens de registro
'''
    logger.debug("Esta é uma mensagem de depuração")
    logger.info("Esta é uma mensagem de informação")
    logger.warning("Esta é uma mensagem de aviso")
    logger.error("Esta é uma mensagem de erro")
    logger.critical("Esta é uma mensagem crítica")
'''

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
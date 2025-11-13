import os

from kubernetes import client, config
from dotenv import load_dotenv


load_dotenv(dotenv_path='./prod.env')
try:
    config.load_incluster_config()
    pass  # 클러스터 내 설정 로드 성공
except Exception as e:
    pass  # 로컬 설정으로 fallback
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    api_server_url = f'https://{os.getenv("MASTER_SERVER")}:6443'
    bearer_token = os.getenv("K8S_BEARER_TOKEN")

    configuration = client.Configuration()
    configuration.host = api_server_url
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": f"Bearer {bearer_token}"}

    client.Configuration.set_default(configuration)
    
    
v1_api = client.CoreV1Api()
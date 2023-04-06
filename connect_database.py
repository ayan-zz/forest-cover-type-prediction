from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
  'secure_connect_bundle': '<<https://datastax-cluster-config-prod.s3.us-east-2.amazonaws.com/25fa037d-54ec-41fa-a738-2a73e353d6ea-1/secure-connect-forest-cover.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2AIQRQ76S2JCB77W%2F20230405%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230405T111445Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=be048c4d18ce6f61539ca811a38897d6034bf153525f75903d46685a87f99770>>secure-connect-forest-cover.zip'
}
auth_provider = PlainTextAuthProvider('<<sZcGEtTmAmmNJszRYHvvkBIN>>', '<<ymnH,SGYC6a_P,,ROSW.Zl0uMhLvbezMLORDrRIvtpH_bZK-93N4w4q90xTPx_TecP7r-lnqpekGcNtB9Fdp3WzFNz-vtwD3K8Gf,JCHbdf4ZWe1YZ9Zb,HKUWCBe5-H>>')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")
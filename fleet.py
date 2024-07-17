import requests
import sqlite3
import math
from dotenv import load_dotenv

load_dotenv()

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
  'Cookie': '%s' % os.getenv('AUTH_COOKIE')
}

db = sqlite3.connect(os.getenv('SQLITE_DB_PATH'))

create_table = """
    create table if not exists agents(
      id TEXT,
      hostname	TEXT,
      cloud_provider	TEXT,
      agent_version	TEXT,
      api_key_name	TEXT,
      cluster_name	TEXT,
      team	TEXT,
      environment	TEXT,
      enabled_products	TEXT,
      remote_config_status	TEXT,
      integrations	TEXT,
      services	TEXT,
      tags	TEXT,
      PRIMARY KEY(id)
    );
    """
db.execute(create_table)


def sanatize(agent):
  for val in agent:
    if agent[val] is not None and type(agent[val]) is list:
      agent[val] = ','.join(filter(None,agent[val]))

def dd_request(url):
  response = requests.request("GET", url, headers=headers)
  return response.json()

def list_all_agent(page=0, total_page=1, entry_per_page = 100 ):
  if not page < total_page :
    return

  url = "https://app.datadoghq.eu/api/ui/remote_config/products/fleet/agents?page_number=%s&page_size=%s&sort_attribute=rc_status&sort_descending=false" % (page, entry_per_page)

  response = dd_request(url)

  agents = response["data"]["attributes"]["agents"]

  for agent in agents:
    url = "https://app.datadoghq.eu/api/ui/remote_config/products/fleet/agents/details/%s" % agent["datadog_agent_key"]

    agent_info = dd_request(url)["data"]["attributes"]
    sanatize(agent)
    sanatize(agent_info)
    try:
      db.execute("INSERT INTO agents VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        agent["datadog_agent_key"], 
        agent["hostname"], 
        agent["cloud_provider"], 
        agent["agent_version"], 
        agent["api_key_name"],
        agent["cluster_name"], 
        agent["team"],
        agent["env"], 
        agent["enabled_products"],
        agent["rc_status"],
        agent["integrations"],
        agent["services"], 
        agent_info["tags"]))
      db.commit()  # Remember to commit the transaction after executing INSERT.
    except sqlite3.Error as error:
      print("Next, ", error)

  total_count = response["meta"]["total_filtered_count"]
  total_page = math.ceil(total_count/entry_per_page)
  list_all_agent(page=(page+1), total_page=total_page)

list_all_agent()

import os
import sys

from piazza_api import Piazza

NOTEBOOKS_DIR = os.path.dirname(__file__)
REPO_DIR = os.path.dirname(NOTEBOOKS_DIR)

sys.path.append(REPO_DIR)

from data_ingestion.settings import piazza_creds

p = Piazza()
p.user_login(email=piazza_creds.PIAZZA_USER_EMAIL, password=piazza_creds.PIAZZA_USER_PASSWORD)
course = p.network("lurzv0qdtfm55d")

x = p._rpc_api.content_instructor_answer(
    params={
        "anonymous": "no",
        "cid": "luz5g88xy27xx",
        "content": "This is an new answer for this question?. Revision 55086086087",
        "revision": 12,
        "type": "i_answer",
        "editor": "rte",
    }
)

print(x)

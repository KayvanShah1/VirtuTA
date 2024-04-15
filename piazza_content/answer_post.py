from piazza_api import Piazza

p = Piazza()
p.user_login()
course = p.network("lurzv0qdtfm55d")

x = p._rpc_api.content_instructor_answer(
    params={
        "anonymous": "no",
        "cid": "luz5g88xy27xx",
        "content": "This is an new answer for this question. Revision 5",
        "revision": 5,
        "type": "i_answer",
        "editor": "rte",
    }
)

print(x)

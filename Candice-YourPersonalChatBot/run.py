from flask import Flask, render_template, request,jsonify
from py2neo import Graph
from neo4j.v1 import GraphDatabase
#chatBot机器人
import QASystemOnKG.chatbot_graph as QAS

app = Flask(__name__)
# graph = Graph('http://localhost:7474', user='neo4j', password='neo4j')
#创建driver对象用于连接数据库
driver =GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","neo4j"))


def buildNodes(nodeRecord): #构建web显示节点
    data = {"id": str(nodeRecord.id), "label": list(nodeRecord.labels)[0]} #将集合元素变为list，然后取出值
    #更新nodeRecord的id
    nodeRecord.properties['id']=str(nodeRecord.id)
    data.update(dict(nodeRecord.properties))

    return {"data": data}

def buildEdges(relationRecord): #构建web显示边
    data = {"id": str(relationRecord.id),
            "source":  str(relationRecord.start),
            "target": str(relationRecord.end),
            "type": str(relationRecord.type)}

    return {"data": data}


@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method=='GET':
        return render_template("home.html")


@app.route("/show")
def show():
    return render_template("index.html")

sql="高血压"

@app.route("/get")
def get_bot_response():
    if request.method== 'GET':
        userText = request.args.get('msg')
        # answer = handler.chat_main(userText)
        # answer = ts.return_ans(userText)
        answer,sql = QAS.get_ans(userText)
        # print("ans:",answer)
        return str(answer)

@app.route("/query")
def query():
    if not request.data:
        return sql
    temp = request.data.decode('utf-8')
    return temp


@app.route('/graph')#两个路由指向同一个网页，返回图的节点和边的结构体
def get_graph():
    with driver.session() as session:
        if(sql!="NULL"):
            temp = 'MATCH (p1)-[r1]-(m) where p1.name=' + "\'" + sql + "\'" +  'RETURN p1,m,r1 limit 20'
            results = session.run(temp).data()
        else:
            results = session.run("MATCH (p1)-[r1]-(m) return p1,r1,m limit 20").data()
        nodeList = []
        edgeList = []
        for result in results:
            nodeList.append(result['p1'])
            nodeList.append(result['m'])
            nodeList = list(set(nodeList))
            edgeList.append(result['r1'])

        nodes = list(map(buildNodes, nodeList))
        edges = list(map(buildEdges, edgeList))
    return jsonify(elements = {"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    app.run(debug = True)

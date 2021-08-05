from flask import Flask, render_template, request,jsonify
from py2neo import Graph
# from neo4j.v1 import GraphDatabase
# import sys
#
# sys.path.append('/Users/sunchao/PycharmProjects/KG/QASystemOnMedicalKG')
# from chatbot_graph import ChatBotGraph
#
#
# handler = ChatBotGraph()


app = Flask(__name__)
graph = Graph('http://localhost:7474', user='neo4j', password='neo4j')
# 构造web显示节点
def buildNodes(nodeRecord):
    data = {"id": nodeRecord.current['n']['id'], "label": list(nodeRecord._labels)[0]} #将集合元素变为list，然后取出值
    data.update(dict(nodeRecord._properties))

    return {"data": data}

def buildEdges(relationRecord): #构建web显示边
    data = {"source": relationRecord.start_node._id,
            "target":relationRecord.end_node._id,
            "relationship": relationRecord.type}

    return {"data": data}
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    # answer = handler.chat_main(userText)
    return str(userText)

@app.route('/graph')
def get_graph():
    # nodes = list(map(buildNodes, graph.run('MATCH (n) RETURN n limit 20')))
    # edges = list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r limit 20')))
    nodes = graph.run('MATCH (n) RETURN n limit 20').data()
    edges = graph.run('MATCH ()-[r]->() RETURN r limit 20').data()
    # return jsonify(elements = {"nodes": nodes, "edges": edges})

    elements = {"nodes": nodes, "edges": edges}
    return elements

@app.route("/example")
def example():
    return render_template("simple-example.html")


if __name__ == "__main__":
    app.run(debug = True)

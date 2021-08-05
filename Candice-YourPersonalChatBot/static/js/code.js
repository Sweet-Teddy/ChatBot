$(document).ready(function(){
//用jQuery的$.get('/graph', function(result) {}, 'json')方法从网站后端的’/graph’路径获得JSON数据存在result中


  $.get('/graph', function(result) {

//
    var style = [
      { selector: 'node', css: {'background-color': '#6FB1FC','content': 'data(name)'}},
      { selector: 'node', css: {'background-color': '#FF0000','content': 'data(name)'}},
       { selector: 'edge', css: {'curve-style': 'bezier','target-arrow-shape': 'triangle', 'content': 'data(type)'}}
    ];

     var cy = cytoscape({
     // DOM容器,决定内容展示的位置,方式一(原生):document.getElementById('xx'),方式二(jQuery):$('#xx')
      container: document.getElementById('cy'),
      style: style,
      layout: { name: 'cose', fit: false },
       // 节点内容,所有的顶点及关系信息的载体
        // 方式一:flat array of nodes and edges,顶点和节点平坦排列
        //方式二：nodes保存所有节点, edges保存所有关系.
      elements: result.elements
    });
  }, 'json');
//   $("submit").click(function(){})
});

from graphviz import Digraph
import os

def build_tree(path, graph, parent=None, ignore=None):
    for item in sorted(os.listdir(path)):
        if ignore and item in ignore:
            continue
        item_path = os.path.join(path, item)
        node_id = item_path.replace("\\", "/")
        graph.node(node_id, item, shape='folder' if os.path.isdir(item_path) else 'note')
        if parent:
            graph.edge(parent, node_id)
        if os.path.isdir(item_path):
            build_tree(item_path, graph, node_id, ignore)

project_path = "Rentix_projects"  # Укажи путь к своему проекту
ignore_list = ['__pycache__', '.venv', '.git']  # Игнорируем лишнее
dot = Digraph(comment='Project Structure', format='png')
build_tree(project_path, dot, ignore=ignore_list)
dot.render('rentix_structure', cleanup=True)

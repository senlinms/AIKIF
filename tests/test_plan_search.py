# test_plan_search.py

import unittest
import sys
import os

root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + 'aikif') 
sys.path.append(root_folder + os.sep + 'lib')

import cls_plan_search as mod_plan

goal =  [1,2,3,4,5,6,7,8,0]
start = [1,2,3,4,5,6,7,0,8]

class PlanSearchTest(unittest.TestCase):
    
    def setUp(self):
        """ Note, this gets called for EACH test """
        unittest.TestCase.setUp(self)
        self.myplan = mod_plan.Plan('8 Puzzle', [], goal, start)
        

    """ 
    tests for plans go below - use myplan instantiated object
    """
    def test_01_new_plan(self):
        self.assertEqual(self.myplan.nme, '8 Puzzle')
        self.assertEqual(len(str(self.myplan)) > 20, True)

    def test_02_check_none_method(self):
        self.assertEqual(self.myplan.nme, '8 Puzzle')
        self.assertEqual(self.myplan.method, 'No method defined')
 
    def test_03_astar_new(self):
        myplan2 = mod_plan.PlanSearchAStar('8 Puzzle', [], goal, start)
        self.assertEqual(myplan2.method, 'A*')
        myplan2.search()   
        self.assertEqual(mod_plan.list_2_str(['1','2']), '1, 2')
        
        self.assertEqual(myplan2.heuristic_cost((1,1),(3,3)),4)
        self.assertEqual(myplan2.heuristic_cost((1,1),(11,11)),20)

        self.assertEqual(myplan2.get_min_f_score(),1)

    def test_05_problem_definition(self):
        prob1 = mod_plan.Problem([1,2,3,4],[3,2,1,4], ['L:-1','R:+1'], 'test1')
        self.assertEqual(len(str(prob1)) > 20, True)
        #self.assertEqual(prob1.goal_test([1,2,3,4]), True)
        
        # check for no actions
        prob1a = mod_plan.Problem([1,2,3,4],[3,2,1,4], [], 'test1a')
        self.assertEqual(len(str(prob1a)) > 20, True)
        
        
    def test_06_problem_goal_test(self):
        prob2 = mod_plan.Problem([1,2,3,4],[3,2,1,4], [], 'test2')
        self.assertEqual(prob2.name, 'test2')
        self.assertEqual(prob2.start, [3,2,1,4])
        self.assertEqual(prob2.goal,  [1,2,3,4])
        
        self.assertEqual(prob2.goal_test('ARE WE THERE YET?'), False)
        self.assertEqual(prob2.goal_test([1,2,3,4]), True)
        self.assertEqual(prob2.goal_test([3,1,3,4]), False)
        
    def test_07_problem_cost(self):
        prob3 = mod_plan.Problem([1,2,3,4],[3,2,1,4], [], 'test3')
        self.assertEqual(prob3.path_cost(), 1)
        
    def test_08_get_successors(self):
        prob3 = mod_plan.Problem([1,2,3,4],[3,2,1,4], [], 'test3')
        self.assertEqual(prob3.get_successors(), [['x1', 50], ['x2', 24], ['x3', 545], ['x5', 32.1]])
        
    def test_10_util_BFS(self):
        graph = {
                'A': ['B', 'E'],
                'B': ['H', 'C', 'D'],
                'E': ['M'],
                'H': ['J', 'M', 'F'],
                'F': [ 'I'],
                'M': [ 'J'],
                'J': ['Z']
                 }
        self.assertEqual(mod_plan.find_path_BFS(graph, 'A', 'B'), ['A', 'B'])
        self.assertEqual(mod_plan.find_path_BFS(graph, 'A', 'F'), ['A', 'B', 'H', 'F'])
        self.assertEqual(mod_plan.find_path_BFS(graph, 'B', 'H'), ['B', 'H'])
        self.assertEqual(mod_plan.find_path_BFS(graph, 'E', 'J'), ['E', 'M', 'J'])
        self.assertEqual(mod_plan.find_path_BFS(graph, 'D', 'Z'), None)

    """
    def test_20_graph_01(self):
        g = mod_plan.ds.Graph({'1': ['2','3','4'], '2':['6','7']})
        mat = g.get_adjacency_matrix()
        self.assertEqual(g.nodes, ['1', '2', '3', '4', '6', '7'])
        
      #  expected = [['1', '2'], ['1', '3'], ['1', '4'], ['2', '6'], ['2', '7']]
        expected = [['2', '6'], ['2', '7'], ['1', '2'], ['1', '3'], ['1', '4']]
        
        # stuff it - keeps changing with random results. self.assertEqual(g.links, sorted(expected)) # sometimes returned in diff order. 
        
      #  self.assertEqual(g.links, sorted(expected)) # sometimes returned in diff order. check
        
        
    def test_20_graph_02(self):
        g = mod_plan.ds.Graph({'animal': ['bird','reptile','insect'], 'bird':['finch','owl'], 'reptile': ['snake', 'lizard'], 'insect': ['ladybird', 'moth']})
        mat = g.get_adjacency_matrix(True)
        self.assertEqual(g.nodes, ['animal', 'bird', 'finch', 'insect', 'ladybird', 'lizard', 'moth', 'owl', 'reptile', 'snake'])
    """
    

if __name__ == '__main__':
    unittest.main()
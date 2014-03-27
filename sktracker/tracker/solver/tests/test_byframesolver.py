from sktracker import data
from sktracker.tracker.cost_function import BrownianCostFunction
from sktracker.tracker.cost_function import DiagCostFunction
from sktracker.tracker.solver import ByFrameSolver

def test_byframe_solver(self):

    trajs = data.brownian_trajs_df()
    cost_functions = {'link': BrownianCostFunction({'max_speed': 5.}),
                  'birth': DiagCostFunction({'cost':10.}),
                  'death': DiagCostFunction({'cost':10.})}
    solver = ByFrameSolver(trajs, cost_functions)
    solver.track()
    

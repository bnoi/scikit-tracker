from sktracker import data

from sktracker.tracker.cost_function.brownian import BrownianCostFunction
from sktracker.tracker.cost_function import DiagCostFunction
from sktracker.tracker.solver import ByFrameSolver
from sktracker.tracker.utils import get_scores_on_trajectories


def test_get_scores_on_trajectories():

    true_trajs = data.brownian_trajs_df()

    cost_functions = {'link': BrownianCostFunction({'max_speed': 5.}),
                      'birth': DiagCostFunction({'cost': 5**2}),
                      'death': DiagCostFunction({'cost': 5**2})}

    solver = ByFrameSolver(true_trajs, cost_functions)

    trajs = solver.track()

    min_chi_square, conserved_trajectories_number, scores = get_scores_on_trajectories(trajs)

    assert min_chi_square == 0 and conserved_trajectories_number == 1

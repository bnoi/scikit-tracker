import pandas as pd

from nose.tools import assert_raises

from sktracker import data

from sktracker.tracker.solver import AbstractSolver
from sktracker.tracker.cost_function import AbstractLinkCostFunction
from sktracker.tracker.cost_function import AbstractDiagCostFunction
from sktracker.tracker.cost_function import BrownianCostFunction


def test_solver_check_cost_function_type():

    trajs = pd.DataFrame([])
    solver = AbstractSolver(trajs)
    cost_function = BrownianCostFunction(parameters={'max_speed': 1})

    solver.check_cost_function_type(cost_function, AbstractLinkCostFunction)

    assert True


def test_solver_check_cost_function_type_failure():

    trajs = pd.DataFrame([])
    solver = AbstractSolver(trajs)
    cost_function = BrownianCostFunction(parameters={'max_speed': 1})

    assert_raises(TypeError, solver.check_cost_function_type, cost_function, AbstractDiagCostFunction)


def test_solver_check_trajs_df_structure():

    trajs = data.brownian_trajs_df()
    solver = AbstractSolver(trajs)

    solver.check_trajs_df_structure(index=['t_stamp', 'label'])
    solver.check_trajs_df_structure(columns=['x', 'y', 't'])

    assert True


def test_solver_check_trajs_df_structure_failure():

    trajs = data.brownian_trajs_df()
    solver = AbstractSolver(trajs)

    assert_raises(ValueError, solver.check_trajs_df_structure, ['t_wrong_stamp', 'label'])

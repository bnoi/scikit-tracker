# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import matplotlib.pyplot as plt

'''
This module provide utility function to represent the trajectories
with matplotlib

'''

def plot_3coords(trajs, coords=('x', 'y', 'z'),
                 text=True, fig=None, **kwargs):
    '''
    Soon to be deprecated, use `plot_stacked_coords` instead
    '''
    return plot_stacked_coords(trajs, coords=coords,
                               text=text, fig=fig, **kwargs)


def plot_stacked_coords(trajs, coords=('x', 'y', 'z'),
                        text=False, fig=None, **kwargs):  # pragma: no cover
    '''
    Plots stacked graphs with each of the coordinates given in the
    `coords` argument plotted against time.

    Parameters
    ----------
    trajs: a :class:`Trajectories` instance
    coords: a tuple, default ('x', 'y', 'z')
        the coordinates (`trajs` column names) to be ploted
    text: bool, default False
        if True, will append each trajectory segment's label
        at the extremities on the upper most plot
    fig: a matplotlib `Figure`, default `None`
        the figure on which to plot

    Returns
    -------
    axes: a list of :class:`matplotlib.axes.Axes`

    '''
    if fig is None:
        # Create a figure with 3 graphs verticaly stacked
        fig, axes = plt.subplots(len(coords), 1, sharex=True, figsize=(6, 9))
    else:
        axes = fig.get_axes()

    for coord, ax in zip(coords, axes):
        trajs.show('t', coord, ax=ax, **kwargs)
        ax.set_ylabel('{} coordinate'.format(coord))
        ax.set_title('')
        ax.set_xlabel('')

    if text:
        for label, segment in trajs.iter_segments:
            axes[0].text(segment.t.iloc[0],
                         segment[coords[0]].iloc[0], str(label))
            axes[0].text(segment.t.iloc[-1],
                         segment[coords[0]].iloc[-1], str(label))

    axes[-1].set_xlabel('Time')

    fig.tight_layout()
    plt.draw()
    return axes


def show_4panels(trajs, label, coords=('x', 'y', 'z'),
                 axes=None, ax_3d=None,
                 scatter_kw={}, line_kw={},
                 interpolate=False, interp_kw={}):  # pragma: no cover
    '''
    Plots the segment of trajectories `trajs` with label `label` on four panels
    organized in two cols by two rows like so:


        y|     y|
         |___   |___
           x      z
        z|     z| y
         |___   |/__
           x      x


    Parameters
    ----------
    trajs: a :class:`Trajectories` instance
    label: int
       the label of the trajectories's segment to plot
    coords: a tuple of column names
       default to ('x', 'y', 'z'), the coordinates to plot
    axes: the axes to plot on
    ax_3d: the 3D ax on the lower right corner
    scatter_kw: dict
       keyword arguments passed to the `plt.scatter` function
    line_kw: dict
       keyword arguments passed to the `plt.plot` function
    interpolate: bool
       if True, will plot the line as an interpolation of
       the trajectories (not implemented right now)
    interp_kw: dict
       keyword arguments for the interpolation

    Returns
    -------

    axes, ax3d: the 2D and 3D axes
    '''
    u, v, w = coords

    segment = trajs.get_segments()[label]

    if interpolate:
        segment_i = trajs.time_interpolate(**interp_kw).get_segments()[label]
    else:
        segment_i = segment

    colors = trajs.get_colors()
    if 'c' not in scatter_kw and 'color' not in scatter_kw:
        scatter_kw['c'] = colors[label]
    if 'c' not in line_kw and 'color' not in line_kw:
        line_kw['c'] = colors[label]

    if axes is None:
        fig, axes = plt.subplots(2, 2, sharex='col',
                                 sharey='row', figsize=(6, 6))
        axes[1, 1].axis('off')
        try:
            ax_3d = fig.add_subplot(224, projection='3d')
        except:
            ax_3d = None

    for ax in axes.ravel():
        ax.set_aspect('equal')
    axes[0, 0].scatter(segment[u].values,
                       segment[v].values, **scatter_kw)
    axes[0, 1].scatter(segment[w].values,
                       segment[v].values, **scatter_kw)
    axes[1, 0].scatter(segment[u].values,
                       segment[w].values, **scatter_kw)
    if ax_3d is not None:
        ax_3d.scatter(segment[u].values,
                      segment[v].values,
                      segment[w].values, **scatter_kw)

    axes[0, 0].plot(segment_i[u].values,
                    segment_i[v].values, **line_kw)
    axes[0, 1].plot(segment_i[w].values,
                    segment_i[v].values, **line_kw)
    axes[1, 0].plot(segment_i[u].values,
                    segment_i[w].values, **line_kw)
    if ax_3d is not None:
        ax_3d.plot(segment_i[u].values,
                   segment_i[v].values,
                   zs=segment_i[w].values, **line_kw)

    axes[0, 0].set_ylabel(u'y position (µm)')
    axes[1, 0].set_xlabel(u'x position (µm)')
    axes[1, 0].set_ylabel(u'z position (µm)')

    axes[0, 0].set_ylabel(u'y position (µm)')
    axes[0, 1].set_xlabel(u'z position (µm)')
    if ax_3d is not None:
        ax_3d.set_xlabel(u'x position (µm)')
        ax_3d.set_ylabel(u'y position (µm)')
        ax_3d.set_zlabel(u'z position (µm)')

    return axes, ax_3d

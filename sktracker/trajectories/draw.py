import matplotlib.pyplot as plt


def plot_3coords(trajs, coords=('x', 'y', 'z'),
                 text=True, fig=None, **kwargs):  # pragma: no cover

    xcoord, ycoord, zcoord = coords
    if fig is None:
        # Create a figure with 3 graphs verticaly stacked
        fig, (ax_x, ax_y, ax_z) = plt.subplots(3, 1, sharex=True, figsize=(6, 9))
    else:
        (ax_x, ax_y, ax_z) = fig.get_axes()
    # Plot each segment x, y and z positions
    trajs.show('t', 'x', ax=ax_x, **kwargs)
    trajs.show('t', 'y', ax=ax_y, **kwargs)
    trajs.show('t', 'z', ax=ax_z, **kwargs)

    if text:
        for label, segment in trajs.iter_segments:
            ax_x.text(segment.t.iloc[0], segment.x.iloc[0], str(label))
            ax_x.text(segment.t.iloc[-1], segment.x.iloc[-1], str(label))

    ax_x.set_ylabel(u'x position')
    ax_x.set_title('')
    ax_x.set_xlabel('')


    ax_y.set_ylabel(u'y position')
    ax_y.set_title('')
    ax_y.set_xlabel('')

    ax_z.set_ylabel(u'z position')
    ax_z.set_xlabel('Time')
    ax_z.set_title('')

    fig.tight_layout()
    plt.draw()
    return (ax_x, ax_y, ax_z)


def show_4pannels(trajs, label, coords=('x', 'y', 'z'),
                  axes=None, ax_3d=None,
                  scatter_kw={}, line_kw={},
                  smth=0, smoothing=0):  # pragma: no cover


    u, v, w = coords

    segment = trajs.get_segments()[label]

    if smoothing != 0:
        raise NotImplementedError
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

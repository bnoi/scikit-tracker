import matplotlib.pyplot as plt


def plot_3coords(trajs, coords=('x', 'y', 'z'),
                 text=True, fig=None, ls='-o', **kwargs):  # pragma: no cover

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

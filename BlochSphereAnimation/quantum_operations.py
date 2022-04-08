from qutip.qip import operations as qops


def qops_rh(angle):
    """
    Rotate state around the "Hadamard axis" (vector 45° w.r.t. z and x-axis in xz-plane)

    Parameters
    ----------
    angle : float
        Rotation angle in radians

    Returns
    -------
    QuTiP operator, Quantum object: dims = [[2], [2]], shape = (2, 2), type = oper
    2x2 matrix
    """
    return qops.rotation(qops.hadamard_transform(), angle)

import qutip

import numpy as np
import matplotlib as mpl
import imageio
from dataclasses import dataclass


def flatten(t):
    """
    Flattens the list t
    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists

    Returns
    -------
    list
        Flattened list
    """
    return [item for sublist in t for item in sublist]


class Sequence:
    def __init__(self, state_start=qutip.basis(2, 0), title=None):
        self.title = title
        self.states = []
        self.texts = []
        self.state_start = state_start
        self.state_current = state_start  # keeps track of the current state
        self.angles = np.linspace(0, np.pi, 20)
        self.state_vector_color = 'r'
        self.vector_constant = None
        self.vector_constant_color = None

    @property
    def length(self):
        return len(self.states)

    def apply_gate(self, rotation_operator):
        """
        Apply the qubit rotation around the 'rotation operator'
        Parameters
        ----------
        rotation_operator : qutip.qip.operations
            E.g. rx, ry, qops_rh
            See: https://qutip.org/docs/latest/apidoc/functions.html
        """
        state_start = self.state_start
        for angle in self.angles:
            state_new = rotation_operator(angle)*state_start
            self.add_state(state_new)
        self.state_current = state_new

    def add_state(self, state, text=None):
        self.states.append(state)
        self.texts.append(text)


@dataclass
class AnimationParameters:
    duration: float = 0.1
    save_all_images: bool = False
    save_first_last_image: bool = True
    filename: str = 'bloch_animation.gif'


class BlochSphereAnimation:
    def __init__(self):
        self._bloch = qutip.Bloch()
        self.animation_parameters = AnimationParameters()
        self._sequences = []
        self._state_current = qutip.basis(2, 0)

    # only setter, without getter
    def view(self, val):
        self._bloch.view = val
    view = property(None, view)

    @property
    def state_current(self):
        return self._state_current

    @state_current.setter
    def state_current(self, state):
        self._state_current = state

    @property
    def number_states(self):
        """
        Returns
        -------
        int
            Total number of states in all sequences
        """
        n = 0
        for sequence in self._sequences:
            n += len(sequence.states)
        return n

    def _reset_bloch(self):
        """
        Resets the Bloch sphere
        """
        self._bloch.make_sphere()
        self._bloch.clear()

    def apply_gate(self, rotation_operator, phase=np.pi, steps=20, vector=None, title=None):
        """
        Apply the qubit rotation around the 'rotation operator'
        Parameters
        ----------
        rotation_operator : qutip.qip.operations
            E.g. rx, ry, qops_rh
            See: https://qutip.org/docs/latest/apidoc/functions.html
        phase : float
            Phase angle by which the gate is performed. Defaults to np.pi
        steps : int
            Number of steps shown in the animations for this gate sequence
        vector : qutip.qobj.Qob or 3d list
            Specifying constant vector to be displayed. Defaults to None.
        title : str
            Title for the sequence, to be displayed in the animation. Defaults to None.
        """
        seq = Sequence(self.state_current, title=title)
        seq.angles = np.linspace(0, phase, steps)
        seq.vector_constant = vector
        seq.vector_constant_color = 'g'
        seq.apply_gate(rotation_operator)
        self.state_current = seq.state_current
        self.add_sequence(seq)

    def add_sequence(self, sequence):
        """
        Adds a sequence to the list of sequences.

        Parameters
        ----------
        sequence : Sequence
            Sequence to be added
        """
        self._sequences.append(sequence)

    def animate(self):
        # Adapted from https://sites.google.com/site/tanayroysite/articles/bloch-sphere-animation-using-qutip

        self._reset_bloch()
        # normalize colors to the length of data
        nrm = mpl.colors.Normalize(0, self.number_states)
        colors = mpl.cm.cool(nrm(range(self.number_states)))  # options: cool, summer, winter, autumn etc.

        # customize sphere properties
        self._bloch.point_color = list(colors)  # options: 'r', 'g', 'b' etc.
        self._bloch.point_marker = ['o']
        self._bloch.point_size = [30]
        self._bloch.vector_width = 4
        #self._bloch.vector_color = [seq.state_vector_color for seq in self._sequences]

        images = []
        all_states = flatten(seq.states for seq in self._sequences)  # flattened list containing all states
        all_states_idx = 0  # counter over all states
        for seq_idx, sequence in enumerate(self._sequences):
            for i in range(sequence.length):
                self._bloch.clear()
                self._bloch.vector_color = [sequence.state_vector_color, sequence.vector_constant_color]
                self._bloch.add_annotation([0, 0, -1.45], sequence.title)

                # Add states
                self._bloch.add_states(sequence.states[i])
                #self._bloch.add_states(sequence.states[:(i+1)], 'point')  # This line only displays the point in the current sequence
                self._bloch.add_states(all_states[:(all_states_idx+1)], 'point')  # This line displays all points in all sequences

                # if sequence.texts[i] is not None:
                #    self._bloch.add_annotation([0, 1, 1.4], sequence.texts[i])
                # Add constant vector
                if sequence.vector_constant is not None:
                    if type(sequence.vector_constant) == qutip.qobj.Qobj:
                        self._bloch.add_states(sequence.vector_constant)
                    else:
                        self._bloch.add_vectors(sequence.vector_constant)



                if self.animation_parameters.save_all_images:
                    filename = "tmp/bloch_%01d.png" % i
                    self._bloch.save(filename)
                    #bloch.save(dirc='tmp')  # saving images to tmp directory
                else:
                    filename = '~temp_file.png'
                    self._bloch.save(filename)
                    if seq_idx == 0 and i == 0 and self.animation_parameters.save_first_last_image:
                        self._bloch.save('bloch_anim_first.png')
                images.append(imageio.imread(filename))
                all_states_idx += 1
        if self.animation_parameters.save_first_last_image:
            self._bloch.save('bloch_anim_last.png')
        imageio.mimsave(self.animation_parameters.filename, images, duration=self.animation_parameters.duration)

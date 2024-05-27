class FlowManager:
    INITIAL = 'initial'

    def __init__(self):
        self.state = FlowManager.INITIAL

    def transition_to(self, new_state):
        self.state = new_state
        print(f"Transitioned to {new_state}")
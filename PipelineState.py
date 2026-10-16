
from transitions import Machine


class IncidentStateMachine:
    states = [
        "DETECTED",
        "COLLECTING_EVIDENCE",
        "DIAGNOSING",
        "PROPOSING_FIX",
        "POLICY_CHECK",
        "AWAITING_APPROVAL",
        "VALIDATING",
        "RECHECKING_CI",
        "HEALED",
        "ESCALATED",
    ]

    transitions = [
        {"trigger": "collect_evidence", "source": "DETECTED", "dest": "COLLECTING_EVIDENCE"},
        {"trigger": "evidence_collected", "source": "COLLECTING_EVIDENCE", "dest": "DIAGNOSING"},
        {"trigger": "diagnosis_complete", "source": "DIAGNOSING", "dest": "PROPOSING_FIX"},
        {"trigger": "fix_proposed", "source": "PROPOSING_FIX", "dest": "POLICY_CHECK"},
        {"trigger": "policy_passed", "source": "POLICY_CHECK", "dest": "VALIDATING"},
        {"trigger": "approval_required", "source": "POLICY_CHECK", "dest": "AWAITING_APPROVAL"},
        {"trigger": "approved", "source": "AWAITING_APPROVAL", "dest": "VALIDATING"},
        {"trigger": "rejected", "source": "AWAITING_APPROVAL", "dest": "ESCALATED"},
        {"trigger": "validation_passed", "source": "VALIDATING", "dest": "RECHECKING_CI"},
        {"trigger": "validation_failed", "source": "VALIDATING", "dest": "ESCALATED"},
        {"trigger": "ci_passed", "source": "RECHECKING_CI", "dest": "HEALED"},
        {"trigger": "ci_failed", "source": "RECHECKING_CI", "dest": "ESCALATED"},
    ]

    def __init__(self):
        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial="DETECTED",
            auto_transitions=False,
        )


if __name__ == "__main__":
    sm = IncidentStateMachine()

    print(sm.state)  # DETECTED

    sm.collect_evidence()
    print(sm.state)  # COLLECTING_EVIDENCE

    sm.evidence_collected()
    print(sm.state)  # DIAGNOSING
    sm.evidence_collected()

    sm.diagnosis_complete()
    print(sm.state)  # PROPOSING_FIX

    sm.fix_proposed()
    print(sm.state)  # POLICY_CHECK

    sm.policy_passed()
    print(sm.state)  # VALIDATING

    sm.validation_passed()
    print(sm.state)  # RECHECKING_CI

    sm.ci_passed()
    print(sm.state)  # HEALED

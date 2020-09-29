import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def pytest_sessionstart(session):
    """placeholder for session start"""
    """ before session.main() is called. """
    if not os.path.exists("json_output"):
        os.makedirs("json_output")
    if not os.path.exists("delta_output"):
        os.makedirs("delta_output")

def pytest_sessionfinish(session, exitstatus):
    """placeholder for session start"""
    """ whole test run finishes. """
    pass

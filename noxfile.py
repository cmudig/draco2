import nox
from nox import session

@nox.session(python="3.7")
def coverage(session: session) -> None:
    """Upload coverage data."""
    # install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
from vtx.gateway_policy import GatewayGrant, GatewayRequest
from vtx.token_ceremony import dry_run


DIGEST = "sha256:" + ("a" * 64)


def request(repository="aevespers2/0", branch="muse/proposal/smoke", operation="contents.write"):
    return GatewayRequest(
        actor="muse",
        repository=repository,
        operation=operation,
        branch=branch,
        payload_digest=DIGEST,
        vtx_envelope_id="vtx-envelope-smoke-0001",
        nonce="nonce-smoke-00000001",
    )


def test_dry_run_proves_allow_and_denial_paths():
    grant = GatewayGrant(
        actor="muse",
        repositories=frozenset({"aevespers2/0"}),
        operations=frozenset({"contents.write"}),
        branch_prefix="muse/proposal/",
    )
    report = dry_run(grant, [
        ("proposal_write", request(), True),
        ("main_denial", request(branch="main"), False),
        ("trust_core_denial", request(repository="aevespers2/1"), False),
        ("workflow_denial", request(operation="workflow.dispatch"), False),
    ])
    assert report.ready_for_live_drill
    assert all(check.passed for check in report.checks)

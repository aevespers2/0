from vtx.gateway_policy import GatewayGrant, GatewayRequest, authorize


DIGEST = "sha256:" + ("a" * 64)


def grant():
    return GatewayGrant(
        actor="muse",
        repositories=frozenset({"aevespers2/0"}),
        operations=frozenset({"contents.read", "contents.write", "branch.create", "pull_request.create"}),
        branch_prefix="muse/proposal/",
    )


def request(**overrides):
    values = dict(
        actor="muse",
        repository="aevespers2/0",
        operation="contents.write",
        branch="muse/proposal/task-001",
        payload_digest=DIGEST,
        vtx_envelope_id="vtx-envelope-00000001",
        nonce="nonce-00000000000001",
    )
    values.update(overrides)
    return GatewayRequest(**values)


def test_proposal_branch_write_is_allowed():
    assert authorize(request(), grant()).allowed


def test_repository_one_is_hard_denied():
    decision = authorize(request(repository="aevespers2/1"), grant())
    assert not decision.allowed
    assert decision.reason == "trust_core_denied"


def test_main_branch_is_denied():
    decision = authorize(request(branch="main"), grant())
    assert not decision.allowed
    assert decision.reason == "branch_denied"


def test_arbitrary_operation_is_denied():
    decision = authorize(request(operation="workflow.dispatch"), grant())
    assert not decision.allowed
    assert decision.reason == "operation_denied"


def test_inactive_grant_is_kill_switch():
    inactive = GatewayGrant(
        actor="muse",
        repositories=frozenset({"aevespers2/0"}),
        operations=frozenset({"contents.write"}),
        branch_prefix="muse/proposal/",
        active=False,
    )
    assert authorize(request(), inactive).reason == "grant_inactive"

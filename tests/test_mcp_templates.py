import json
from pathlib import Path


def test_lifetime_platform_insights_are_not_numeric_network_catalog():
    insights = json.loads(Path("packages/lifetime-network-mcp-server/data/platform_insights.json").read_text())
    assert "ecosystemNodes" in insights
    assert "app_platform" in insights["ecosystemNodes"]
    assert "TV Everywhere" in insights["platforms"]


def test_mcp_fabric_packages_are_public_ready():
    for package_path in [
        Path("packages/communication-fabric-mcp-template/package.json"),
        Path("packages/lifetime-network-mcp-server/package.json"),
    ]:
        package = json.loads(package_path.read_text())
        assert package["private"] is False
        assert package["license"] == "MIT"
        assert "build" in package["scripts"]


def test_lifetime_server_exposes_advanced_fabric_primitives():
    server = Path("packages/lifetime-network-mcp-server/src/server.ts").read_text()
    for primitive in [
        "search_lifetime_graph",
        "summarize_relationship_network",
        "draft_communication",
        "create_evidence_packet",
        "classify_document_sensitivity",
        "request_user_consent",
        "generate_project_timeline",
        "secure_message_drafter",
        "agent_handoff_summary",
        "project_state_reconstructor",
    ]:
        assert primitive in server
    assert "Never bypass authentication" in server

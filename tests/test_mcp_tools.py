"""Tests for MCP tools loading with per-user authentication."""

import pytest

from src.agents.aws_rds_instance_creator.mcp_tools import load_mcp_tools


class TestLoadMcpTools:
    """Test the load_mcp_tools function with per-user authentication."""

    @pytest.mark.anyio
    async def test_load_mcp_tools_without_token_none(self):
        """Test that load_mcp_tools fails when token is None."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools(None)

    @pytest.mark.anyio
    async def test_load_mcp_tools_without_token_empty_string(self):
        """Test that load_mcp_tools fails when token is empty string."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools("")

    @pytest.mark.anyio
    async def test_load_mcp_tools_without_token_whitespace(self):
        """Test that load_mcp_tools fails when token is only whitespace."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools("   ")

    @pytest.mark.anyio
    async def test_load_mcp_tools_with_invalid_token(self):
        """Test that load_mcp_tools raises RuntimeError with invalid token.
        
        Note: This test requires network access to the MCP server and will fail
        if the token is invalid or MCP server is not accessible. In CI/CD, this
        test should be mocked or skipped.
        """
        invalid_token = "invalid-jwt-token"
        
        # This should raise RuntimeError because the MCP server will reject the token
        with pytest.raises(RuntimeError, match="Failed to load MCP tools"):
            await load_mcp_tools(invalid_token)


class TestMcpToolsConfiguration:
    """Test that MCP tools configuration is correct."""

    def test_required_tools_defined(self):
        """Test that required tool names are correctly defined."""
        # Import the module to check the required tools list
        # Read the module source to verify required tools
        import inspect

        from src.agents.aws_rds_instance_creator import mcp_tools
        source = inspect.getsource(mcp_tools)
        
        # Verify all required tools are mentioned
        required_tools = [
            "list_environments_for_org",
            "list_cloud_resource_kinds",
            "get_cloud_resource_schema",
            "create_cloud_resource",
            "search_cloud_resources",
        ]
        
        for tool in required_tools:
            assert tool in source, f"Required tool {tool} not found in mcp_tools.py"

    def test_mcp_server_url_configured(self):
        """Test that MCP server URL is correctly configured."""
        # Import the module to check the URL
        # Read the module source to verify URL
        import inspect

        from src.agents.aws_rds_instance_creator import mcp_tools
        source = inspect.getsource(mcp_tools)
        
        # Verify MCP server URL is correct
        assert "https://mcp.planton.ai/" in source


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


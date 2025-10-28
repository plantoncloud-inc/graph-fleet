<!-- 0ffb1b48-e164-4bf3-bdf8-f12eec30c224 9ce15536-771f-4d2d-85dc-192f4819c36b -->
# Remove Buf Setup from GraphFleet langgraph.json

## Changes Required

### File: `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/langgraph.json`

Update line 13 in the `dockerfile_lines` array to remove the Buf authentication while keeping Git and GitHub configuration:

**Current (line 13):**

```json
"RUN mkdir -p /root && chmod 700 /root && printf \"machine buf.build\\nlogin %s\\npassword %s\\nmachine github.com\\nlogin git\\npassword %s\\n\" \"$BUF_USER\" \"$BUF_API_TOKEN\" \"$GITHUB_TOKEN\" > /root/.netrc && chmod 600 /root/.netrc"
```

**Updated (line 13):**

```json
"RUN mkdir -p /root && chmod 700 /root && printf \"machine github.com\\nlogin git\\npassword %s\\n\" \"$GITHUB_TOKEN\" > /root/.netrc && chmod 600 /root/.netrc"
```

This change:

- Removes the `machine buf.build` entry and its associated credentials (`$BUF_USER` and `$BUF_API_TOKEN`)
- Keeps the Git installation (line 11)
- Keeps the environment variables setup (line 12)
- Keeps the GitHub authentication configuration with the `$GITHUB_TOKEN`
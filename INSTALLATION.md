## Installation & Setup

**Prerequisites:**
   - Python
   - uv (https://docs.astral.sh/uv)
   - A Strava Account
   - Cequence Gateway (optional)

### 1. Strava Account and OAuth Setup

1. Go to [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Create a new application:
   - Enter your application details (name, website, description)
   - Important: 
      - If you are using Cequence Gateway, set the  as `Authorization Callback Domain` as `auth.aigateway.cequence.ai`
      - If you are setting up on `stdio`, set the `Authorization Callback Domain` as `localhost`
   - Note down your Client ID and Client Secret

This is for Local Setup Only:
1. In order to get the access_token, run the following command - 
   ```bash
   python auth_scripts/oauth_flow.py
   ```
2. The above script will ask for your client-id, client-secret
3. Open the url in your browser and give the necessary access
4. After giving permissions, will get a Apache webpage.
5. From the Apache Webpage URL i.e `..../?state=&code=<AUTHORIZATION_CODE>&scope=...`, copy the `AUTHORIZATION_CODE`
6. Paste the code in the terminal
7. An `.env` file with the following tokens will be created

```
STRAVA_ACCESS_TOKEN=...
STRAVA_EXPIRES_AT=...
STRAVA_REFRESH_TOKEN=...
```

### 2. MCP server setup using Cequence AI gateway

1. **Clone Repository:**
   ```bash
   git clone https://github.com/Better-Boy/strava-mcp.git
   cd strava-mcp
   ```

2. **Create Custom App:**
   - Create a custom app using the file `openapi.yaml`. 

3. **Create MCP Server**
   - Create a MCP server using oauth as the authentication and authorization. 
   - Specify `Authorization URL` as `https://www.strava.com/oauth/authorize`
   - Specify `Token URL` as `https://www.strava.com/api/v3/oauth/token`
   - Specify `Client ID` as `your client id`
   - Specify `Client Secret` as `your client secret`
   - Specify `Scopes` as `read,read_all,profile:read_all,activity:read_all` - don't change this as cequence uses spaces for multiple scopes but strava uses comma.

Refer Strava OAuth Documentation - [Strava OAuth Docs](https://developers.strava.com/docs/authentication/)
For further instructions, refer [Cequence Docs](https://docs.aigateway.cequence.ai/docs/getstarted)


### 3. Local MCP Server setup

1. Install `uv`
2. Run the following command

```bash
uv sync
uv run src/strava_server/server.py
```

Now, you can access the mcp server at `http://0.0.0.0:8000/mcp` and the fastapi server at the `http://0.0.0.0:8000`.


### 4. MCP Client setup

- If using cequence, add the following,

   ```json
   {
      "mcpServers": {
         "strava": {
            "command": "npx",
            "args": [
            "-y",
            "@cequenceai/mcp-remote",
            "<MCP_ENDPOINT>"
            ]
         }
   }
   ```
- If using stdio, add the following,

You can either use the `.env` to set the token, or pass the token in the form of headers.

```json
    {
      "mcpServers": {
         "strava": {
            "type": "streamable-http",
            "url": "http://localhost:8000/mcp",
            "headers": {
               "authorization": "Bearer <token>"
            }
         }
   }
```
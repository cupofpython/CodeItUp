# CodeItUp

This is a Slack App that leverages the GitLab Code Suggestions API to write code from you from Slack!

## How to use this code

To set it up locally, check out this project and follow these steps:

### Run the local server
1. Run the command `python3 bot.py` in your Terminal

### Set up ngrok
1. Install ngrok
1. Open a separate Terminal
1. Run the command `ngrok http 5000`

This creates a tunnel to the local server.

### Create a new Slack Bot
1. Create a Slack Bot for your workspace at api.slack.com
1. Update the manifest to this, replacing `[YOUR_NGROK_URL]` to the one generated in the last step:

```
display_information:
  name: CodeItUp
features:
  bot_user:
    display_name: CodeItUp
    always_online: false
  slash_commands:
    - command: /generate
      url: [YOUR_NGROK_URL]/generate
      description: Generates a code suggestion
      usage_hint: "file: [file name];prompt: [prompt]; token: [token]"
      should_escape: false
oauth_config:
  scopes:
    bot:
      - chat:write
      - chat:write.customize
      - files:write
      - channels:read
      - commands
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
  ```

### Invite the slack bot to the channel
1. Invite your Slack bot to your workspace's channel

### Create a Personal Access Token
1. Create a GitLab PAT with `api` and `ai_features` scope
1. Save the generated token for the next step

### Test out the Bot
1. Test the bot with the following command:
`/generate file: helloworld.py; prompt: Write a python script that says hello world; token: [YOUR_PERSONAL_ACCESS_TOKEN]`

   * All commands should follow this format: `/generate file: [FILE_NAME]; prompt: [SOME_PROMPT]; token: [YOUR_PERSONAL_ACCESS_TOKEN]`

## Project Info
- Developer: [Sam Morris](https://gitlab.com/sam)
- Tools: Python, ngrok, Slack, GitLab APIs

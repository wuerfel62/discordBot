# Bot Documentation
A bot for role management for now. It is somewhat customizabe in discord itself. 

## required files

* channel.conf and roles.conf in json format
* token.sec for Discord-Bot token
    * as plain text

## commands

### role-management
can only be used in the config text-channel
* !role-add "role name" "emoji"
    * adds a new role to the role management
* !role-remove "role name"
    * removes role from role management
* !regen-roles
    * regenerates the role message in the roles text-channel
    * purges/removes all messages in the roles channel

### bot-config
these commands are used to change the text-channels the bot uses. For now the bot has to be restartet for the changes to take effect.
* !set-log-channel
    * used for logs from bot
* !set-role-channel
    * sets the channel for role management
    * gets purged (all messages get deleted)
* !set-config-channel
    * sets the channel for bot configuration
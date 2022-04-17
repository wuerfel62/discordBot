# Bot Documentation
A bot for role management for now. It is somewhat customizabe in discord itself. 

## required files

* channel.conf and roles.conf in json format
    * will be automaticly created at first startup
* token.sec for Discord-Bot token
    * as plain text
    * has to be there for the bot to start

## commands

### role-management
can only be used in the config text-channel
* !addRole "role name" "emoji"
    * adds a new role to the role management
* !removeRole "role name"
    * removes role from role management
* !regenRoles
    * regenerates the role message in the roles text-channel
    * purges/removes all messages in the roles channel

### bot-config
these commands are used to change the text-channels the bot uses. For now the bot has to be restartet for the changes to take effect.
* !setLogChannel
    * used for logs from bot
* !setRoleChannel
    * sets the channel for role management
    * gets purged (all messages get deleted)
* !setConfigChannel
    * sets the channel for bot configuration
* !changePrefix "prefix"
    * changes the prefix used for bot commands
* !changeGame "game"
    * changes the game that is diplayed in discord
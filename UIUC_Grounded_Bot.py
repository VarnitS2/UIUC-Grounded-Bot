import discord
from datetime import datetime

client = discord.Client()
ADMIN = "Admin"
BOTS = "Bots"
UIUC_GROUNDED_BOT = "UIUC Grounded Bot"
EVERYONE = "@everyone"
FAIL = "Fail"
SUCCESS = "Success"

clientSecretFileName = "client_secret.txt"
logFileName = "Logs.txt"

def log(message, command, result, failReason="", comments=""):
    with open(logFileName, 'a+') as f:
        if result == SUCCESS:
            f.write('[{}] -> Triggered by: {}\nMessage content: {}\nCommand executed: {}\nResult: {}\nComments: {}\n\n'.format(datetime.now(), message.author, message.content, command, result, comments))
        elif result == FAIL:
            f.write('[{}] -> Triggered by: {}\nMessage content: {}\nCommand executed: {}\nResult: {}\nReason: {}\nComments: {}\n\n'.format(datetime.now(), message.author, message.content, command, result, failReason, comments))

@client.event
async def on_ready():
    print('[{}] - Logged in as {}'.format(datetime.now(), client.user))
    with open(logFileName, 'a+') as f:
        f.write('-------------------- New Session --------------------\n')
        f.write('Time initiated: [{}]\n'.format(datetime.now()))
        f.write('Successfully logged in as {0.user}\n\n'.format(client))

@client.event
async def on_message(message):
    messageList = message.content.split(maxsplit=1)
    channel = message.channel
    user = message.author

    if not (channel.name == 'bot-commands' or channel.name == 'bot-commands-test'):
        log(message, messageList[0], FAIL, failReason="Command not in the #bot-commands.")
        return

    if message.author == client.user:
        return
    
    if messageList[0] == '!hello':
        print('[{}] [{}] - Executed !hello'.format(datetime.now(), user))
        try:
            await channel.send('hello!')
            log(message, messageList[0], SUCCESS)
        except Exception as e:
            await channel.send('There was an error executing the command. This event has been logged.')
            log(message, messageList[0], FAIL, e)
        

    if messageList[0] == '!printpara':
        print('[{}] [{}] - Executed !printpara'.format(datetime.now(), user))
        try:
            await channel.send('Hi there!\n\nThis is a paragraph!')
            log(message, messageList[0], SUCCESS)
        except Exception as e:
            await channel.send('There was an error executing the command. This event has been logged.')
            log(message, messageList[0], FAIL, e)

    if messageList[0] == '!addrole':
        print('[{}] [{}] - Executed !addrole'.format(datetime.now(), user))
        try:
            member = message.author
            role = messageList[1]
            guild = message.guild
            allRoles = guild.roles

            roleAddFlag = False
            roleExistFlag = False
            forbiddenRoleFlag = False
            noRolesFlag = True

            if role == ADMIN or role == BOTS or role == UIUC_GROUNDED_BOT:
                forbiddenRoleFlag = True
            
            for elem in allRoles:
                noRolesFlag = False
                if elem.name == ADMIN or elem.name == BOTS or role == UIUC_GROUNDED_BOT:
                    continue
                if elem.name == role:
                    await member.add_roles(elem)
                    await channel.send('Role added!')
                    roleExistFlag = True
                    roleAddFlag = True

            if noRolesFlag:
                await channel.send('There are no active roles in this server.')
                log(message, messageList[0], SUCCESS, comments="No existing roles.")
            elif forbiddenRoleFlag:
                await channel.send('That role cannot be accessed by members.')
                log(message, messageList[0], SUCCESS, comments="Forbidden role.")
            elif not roleExistFlag:
                await channel.send('That role does not exist.')
                log(message, messageList[0], SUCCESS, comments="Role does not exist.")
            elif roleAddFlag:
                log(message, messageList[0], SUCCESS)
                
        except Exception as e:
            await channel.send('There was an error executing the command. This event has been logged.')
            log(message, messageList[0], FAIL, e)

    if messageList[0] == '!removerole':
        print('[{}] [{}] - Executed !removerole'.format(datetime.now(), user))
        try:
            member = message.author
            role = messageList[1]
            guild = message.guild
            memberRoles = member.roles

            roleRemoveFlag = False
            roleExistFlag = False
            forbiddenRoleFlag = False
            noRolesFlag = True

            if role == ADMIN or role == BOTS or role == UIUC_GROUNDED_BOT:
                forbiddenRoleFlag = True
            
            for elem in memberRoles:
                noRolesFlag = False
                if elem.name == ADMIN or elem.name == BOTS or elem.name == UIUC_GROUNDED_BOT:
                    continue
                if elem.name == role:
                    await member.remove_roles(elem)
                    await channel.send('Role removed!')
                    roleExistFlag = True
                    roleRemoveFlag = True
            
            if noRolesFlag:
                await channel.send('You don\'t have any active roles.')
                log(message, messageList[0], SUCCESS, comments="User has no active roles.")
            elif forbiddenRoleFlag:
                await channel.send('That role cannot be accessed by members.')
                log(message, messageList[0], SUCCESS, comments="Forbidden role.")
            elif not roleExistFlag:
                await channel.send('That role does not exist.')
                log(message, messageList[0], SUCCESS, comments="Role does not exist.")
            elif roleRemoveFlag:
                log(message, messageList[0], SUCCESS)

        except Exception as e:
            await channel.send('There was an error executing the command. This event has been logged.')
            log(message, messageList[0], FAIL, e)

    if messageList[0] == '!allroles':
        print('[{}] [{}] - Executed !allroles'.format(datetime.now(), user))
        try:
            guild = message.guild
            allRoles = guild.roles
            noRolesFlag = True

            reply = '```\nThis is the list of all active roles:'

            for elem in allRoles:
                if elem.name == ADMIN or elem.name == BOTS or elem.name == UIUC_GROUNDED_BOT or elem.name == EVERYONE:
                    continue
                else:
                    reply += '\n' + elem.name
                    noRolesFlag = False

            reply += '\n```'

            if noRolesFlag:
                await channel.send('There are currently no active roles')
                log(message, messageList[0], SUCCESS, comments="No active roles.")
            else:
                await channel.send(reply)
                log(message, messageList[0], SUCCESS)

        except Exception as e:
            await channel.send('There was an error executing the command. This event has been logged.')
            log(message, messageList[0], FAIL, e)

    if messageList[0] == '!help':
        print('[{}] [{}] - Executed !help'.format(datetime.now(), user))
        await channel.send('```This is the help page.\n\nList of commands:\n\t1. !addrole <role name> - Add the role <role name> to yourself.\n\t2. !removerole <role name> - Remove the role <role name> from yourself.\n\t3. !allroles - Display the list of all active roles.```')
        log(message, messageList[0], SUCCESS)


with open(clientSecretFileName) as f:
    client.run(f.readline())
server_commands_status = {
    "ERR_NOT_EXISTENT": "Command doesn't exists."
}

async def command_reset_level(consumer):
    consumer.character.experience = 0
    consumer.character.level = 1
    consumer.character.save()
async def command_get_list(consumer):
    commands = list(server_commands.keys())
    await consumer.send_commands_list(commands)

async def command_get_exp_required_for_level(consumer, level):
    try:
        lvl = int(level)
        await consumer.character.get_exp_required_for_level(lvl)
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)

async def command_get_exp(consumer, experience_points):
    try:
        points = int(experience_points)
        await consumer.character.get_experience(points)
    except ValueError:
        print("must be a value")
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)


server_commands = {
    'exp': command_get_exp,
    'help': command_get_list,
    'lvl': command_get_exp_required_for_level,
    'reset': command_reset_level,
}

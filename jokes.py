from jokeapi import Jokes
import asyncio


async def tell_joke():
  j = await Jokes()
  joke = await j.get_joke()
  if joke["type"] == "single":
    return joke["joke"]
  else:
    return joke["setup"], joke["delivery"]
    
#asyncio.run(tell_joke())
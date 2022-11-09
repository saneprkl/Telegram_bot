from jokeapi import Jokes
import asyncio


async def tell_joke():
  j = await Jokes()
  joke = await j.get_joke()
  if joke["type"] == "single":
    print(joke["joke"])
    return joke["joke"]
  else:
    print(joke["setup"])
    print(joke["delivery"])
    return joke["setup"], joke["delivery"]
    


#asyncio.run(tell_joke())
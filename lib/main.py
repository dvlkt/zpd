import asyncio
import multiprocessing

import api

def main():
	asyncio.run(api.run())

main()
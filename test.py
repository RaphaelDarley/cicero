import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

async def main():

    flow = Flow.from_file("./flows/info_to_facts.ai.yaml").set_vars(info = '''
In 1789 the Viceroy of New Spain, Manuel Antonio Flórez, instructed Martínez to occupy Nootka Sound, on Vancouver Island in present-day British Columbia, build a settlement and fort, and to make it clear that Spain was setting up a formal establishment.[2] The Russians were threatening to take the sound, and in May 1788 the British fur trader John Meares had used Nootka Sound as a base of operations and claimed purchase of land there from the indigenous Nuu-chah-nulth people. Martínez, then ranked piloto primero and alférez de navío (Ensign or Sub-Lieutenant), led an expedition that arrived at Nootka Sound in early 1789. The force consisted of the warship La Princesa, commanded by Martínez, and the supply ship San Carlos (el Filipino), under Gonzalo López de Haro. He gave Nootka Sound the name Puerto de San Lorenzo de Nuca. The expedition built a settlement there named Santa Cruz de Nuca, including houses, a hospital, and the presidio Fort San Miguel.[3]
The Martínez expedition arrived at Nootka Sound on May 5, 1789. During the summer of 1789 a number of fur trading vessels, British and American, arrived at Nootka. The US ships, the Columbia Rediviva and Lady Washington under John Kendrick and Robert Gray were allowed to operate unmolested. Kendrick and Martínez were friendly toward each other and Kendrick provided some assistance to Martínez during the seizure of the Argonaut.[4]
A conflict over violating Spanish sovereignty rights of trade and navigation on the coast arose between the captain of John Meares' British Argonaut, James Colnett and his claim of the Meares company land, and Martínez. By the end of the summer Martínez had arrested Colnett, seized several British ships, and arrested their crews. Martínez and the Spanish departed Nootka Sound in late summer 1789. They returned to San Blas, New Spain, with captured ships, including the British sloop Princess Royal and prisoners. In 1790 a new Spanish expedition under Francisco de Eliza reoccupied Nootka Sound, followed by Alessandro Malaspina in 1791
These events at Nootka Sound led to the Nootka Crisis between the Kingdom of Spain and Kingdom of Great Britain about colonization and territorial access of the Pacific Northwest coast of North America. The crisis nearly led to a war. Spain was looking to France for support but when they refused Spain had to back down and opened negotiations. A series of Nootka Conventions began which led to Spain's capitulation of the area. Subsequently, Martínez lost favor due to his actions in the incident, and a new Viceroy was appointed, Juan Vicente de Güemes, Count of Revillagigedo. Juan Francisco de la Bodega y Quadra diplomatically implemented the Nootka Conventions in 1792 with British explorer George Vancouver.
''')

    #flow = Flow.from_file("./flows/facts_to_truth.ai.yaml")

    res = await flow.run()
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
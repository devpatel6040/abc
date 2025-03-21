# Importing the required libraries.
import requests
import imageLib
import os

# Url of the API.
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get _pokemon_into() function
    # Use breakpoints to view returned dictionary
    # poke_info = get_pokemon_info("Rockruff")
    # poke_info = get_pokemon_info(123)
    names = get_pokemon_names()
    download_pokemon_artwork(names[0], r'C:\temp')
    return

def get_pokemon_info(pokemon_name) :
    """This function collets the data from the api and gives the details of the givee pokemone name.

    Args:
        pokemon_name (str): pokemon name

    Returns:
        Dict: Dictonary of the pokemon's details
    """
    # lowercasing and removing white spaces from the given name.
    pokemon_name = str(pokemon_name).strip().lower()
    
    # creating url 
    url = POKE_API_URL + pokemon_name
    
    print(f'Getting information for {pokemon_name}...', end='')
    #getting data using get function of requestes 
    resp_msg = requests.get(url)
    
    # If sucessfully in fetching data.
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    # Error message if not successfully.
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
    
def get_pokemon_names(offset=0, limit = 100000):
    """This function gives an list of pokemones' names using the api

    Args:
        offset (int, optional): Defaults to 0.
        limit (int, optional): Defaults to 100000.

    Returns:
        list: Returns an list of the pokemon's name
    """
    
    # Dict to set offset and limit.
    query_str_params = {
        'offet' : offset,
        'limit' : limit
    }
    print(f'Getting list of Pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL,params=query_str_params)
    
     # If sucessfully in fetching data.
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        pokemon_dict = resp_msg.json()
        pokemon_names_list = [p['name'] for p in pokemon_dict['results']]
        return pokemon_names_list
    # Error message if not successfully.
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
def download_pokemon_artwork(pokemon_name, save_dir):
    """This function takes an name and folder location with the given name it will find the image of that pokemon and save it to the given location.

    Args:
        pokemon_name (str): Name of pokemon
        save_dir (str): Location of a folder

    Returns:
        None: It does not return any thing it just saves the images of the pokemon after fetching it.
    """
    # Getting information of a particular pokemon.
    pokemon_info = get_pokemon_info(pokemon_name)
    
    # Returning from the function if there is no information.
    if pokemon_info == None:
        return
    
    # Getting the url of the image of the pokemon.
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']
    # Downloading the image.
    image_bytes = imageLib.download_image(artwork_url)
    
    # Returning from the function if there is no image.
    if image_bytes is None:
        return
    
    # If there is a image than saving it with the pokemon's name and with the same extension.
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')
    
    # Saving it to the Given location.
    if imageLib.save_image_file(image_bytes, image_path):
        return image_path

# This from were the execution of the program starts from.
if __name__ == '__main__':
    main()
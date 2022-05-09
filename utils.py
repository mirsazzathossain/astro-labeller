import os
import json
import datetime
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt
from astroquery.vizier import Vizier
from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord


def get_catalog(catalog_name):
    """
    Get a catalog from Vizier.

    Parameters
    ----------
    catalog_name : str
        Name of the catalog to get.
    
    Returns
    -------
    catalog : astroquery.vizier.VizierCatalog
        Catalog to get.
    """

    Vizier.ROW_LIMIT = -1
    catalog = Vizier.get_catalogs(catalog_name)[0]

    return catalog


def get_processed_catalog(catalog):
    """
    Get a catalog with the following columns:
    - FCG
    - RAJ2000
    - DEJ2000

    Parameters
    ----------
    catalog : astroquery.vizier.VizierCatalog
        Catalog to process.

    Returns
    -------
    catalog : pandas.DataFrame
        Catalog with the following columns:
        - FCG
        - RAJ2000
        - DEJ2000
    """
    
    catalog = catalog.to_pandas()
    catalog = catalog[['FCG', 'RAJ2000', 'DEJ2000', 'Com']]
    catalog = catalog[catalog['Com'].str.contains('wat|nat')]
    catalog = catalog.drop_duplicates(subset=['FCG'])
    catalog = catalog.drop(columns=['Com'])
    catalog = catalog.dropna()
    catalog = catalog.reset_index(drop=True)

    return catalog


def fits_to_png(image, png_file):
    """
    Convert a FITS image to a PNG image.

    Parameters
    ----------
    image : array
        FITS image.
    png_file : str
        PNG file to save.
    """

    image = np.array(image)
    image = image[::-1, :]
    image = image[:, ::-1]
    plt.imshow(image)
    plt.axis('off')
    plt.savefig(png_file, dpi=300, bbox_inches='tight', transparent=True, pad_inches=0)
    

def get_single_fits(survey, ra, dec, fileName):
    """
    Get a FITS image from NASA skyview.

    Parameters
    ----------
    survey : str
        Survey name.
    ra : float
        Right ascension.
    dec : float
        Declination.
    fileName : str
        Name of the file to save the image.
    """

    try:
        images = SkyView.get_images(position=str(ra) + ', ' + str(dec), survey=survey, coordinates='J2000', pixels=(150, 150))

        image = images[0][0].data
    except Exception as e:
        print(f'Image not found for {ra} {dec}')

    try:
        fileName = fileName.replace('.fits', '')
        fileName = fileName + '.png'
        fits_to_png(image, fileName)
    except Exception as e:
        print(f'Failed to save the image for {ra} {dec}')


def get_fits_images(catalog, survey, directory):
    """
    Get FITS images from NASA skyview.

    Parameters
    ----------
    catalog : pandas.DataFrame
        Catalog with the following columns:
        - FCG
        - RAJ2000
        - DEJ2000
    survey : str
        Survey name.
    directory : str
        Directory to save the images.
    """

    for i in range(len(catalog)):
        fileName = f'{directory}/{catalog["FCG"][i]}.fits'

        ra = catalog["RAJ2000"][i]
        dec = catalog["DEJ2000"][i]

        try:
            skycoord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
            ra = skycoord.ra.deg
            dec = skycoord.dec.deg
        except:
            print(f'Sky coordinates not found for {catalog["FCG"][i]}')

        get_single_fits(survey, ra, dec, fileName)


def get_undownloaded_images(catalog, directory):
    """
    Get catalog for images that are not downloaded.

    Parameters
    ----------
    catalog : pandas.DataFrame
        Catalog with the following columns:
        - FCG
        - RAJ2000
        - DEJ2000
    directory : str
        Directory to save the images.

    Returns
    -------
    catalog : pandas.DataFrame
        Catalog with the following columns:
        - FCG
        - RAJ2000
        - DEJ2000
    """

    flag = []
    for i in range(len(catalog)):
        flag.append(os.path.isfile(f'{directory}/{catalog["FCG"][i]}.png') == False)

    catalog = catalog[flag]
    catalog = catalog.reset_index(drop=True)

    return catalog


def get_json_catalog(catalog, fileName):
    """
    Get a catalog in JSON format.

    Parameters
    ----------
    catalog : pandas.DataFrame
        Catalog with the all columns.
    fileName : str
        Name of the file to save the catalog.
    """

    catalog = catalog.to_pandas()
    catalog = catalog[catalog['Com'].str.contains('wat|nat')]
    catalog = catalog.drop_duplicates(subset=['FCG'])
    catalog = catalog.reset_index(drop=True)

    with open(fileName, 'w') as f:
        json.dump([], f, indent=4)

    with open(fileName, 'r') as f:
        data = json.load(f)

    for i in range(len(catalog)):
        data.append(
            {
                "model": "app.catalogue",
                "fields": {
                    "fcg": catalog["FCG"][i],
                    "first": catalog["FIRST"][i],
                    "img": catalog["Img"][i],
                    "RAJ2000": catalog["RAJ2000"][i],
                    "DEJ2000": catalog["DEJ2000"][i],
                    "size_arcmin": str(catalog["Size"][i]),
                    "u_size": catalog["u_Size"][i],
                    "type": catalog["Type"][i],
                    "grp": catalog["Grp"][i],
                    "group": catalog["Group"][i],
                    "com": catalog["Com"][i],
                    "tno":  str(catalog["Tno"][i]),
                    "timestamp": str(datetime.datetime.now())
                }
            }
        )

    with open(fileName, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':

    # Get the catalog
    catalog = get_catalog('J/ApJS/194/31')

    # Get the processed catalog
    # processed_catalog = get_processed_catalog(catalog)

    # Get the FITS images
    # get_fits_images(processed_catalog, 'VLA FIRST (1.4 GHz)', 'static_cdn/galaxies')

    # Get the catalog for images that are not downloaded
    # catalog = get_undownloaded_images(processed_catalog, 'static_cdn/galaxies')

    # Get the FITS images for the undownloaded catalog
    # get_fits_images(catalog, 'VLA FIRST (1.4 GHz)', 'static_cdn/galaxies')

    # Get number of downloaded images
    #print(len(os.listdir('static_cdn/galaxies')))

    # Get the catalog in JSON format
    get_json_catalog(catalog, 'app/fixtures/WAT_NAT.json')
import xml.etree.ElementTree as ET
import traceback


def build_item_lookup(localization_dictionary):
    """
    Creates a dictionary of items with the localization provided.
    :return: dictionary of items
    """
    item_xml = ET.parse('libs/game_data/items.xml')
    item_root = item_xml.getroot()
    items = item_root.getchildren()

    """
    Example Item Format: (T2_2H_Bow)
    In [29]: ri
    Out[29]: <Element 'weapon' at 0x7fd2afa6b688>

    In [30]: ri.attrib
    Out[30]: 
    {'abilitypower': '120',
     'activespellslots': '3',
     'attackdamage': '29',
     'attackrange': '11',
     'attackspeed': '1',
     'attacktype': 'ranged',
     'durability': '5647',
     'durabilityloss_attack': '1',
     'durabilityloss_receivedattack': '1',
     'durabilityloss_receivedspell': '1',
     'durabilityloss_spelluse': '1',
     'focusfireprotectionpeneration': '0',
     'fxbonename': 'LeftArm_3',
     'fxboneoffset': '0.2 -0.227 0.135',
     'hitpointsmax': '0',
     'hitpointsregenerationbonus': '0',
     'itempower': '300',
     'itempowerprogressiontype': 'mainhand',
     'magicspelldamagebonus': '0',
     'mainhandanimationtype': 'bow',
     'maxqualitylevel': '5',
     'passivespellslots': '1',
     'physicalspelldamagebonus': '0',
     'shopcategory': 'ranged',
     'shopsubcategory1': 'bow',
     'slottype': 'mainhand',
     'tier': '2',
     'twohanded': 'true',
     'uiatlas': 'RefItemAtlas',
     'uniquename': 'T2_2H_BOW',
     'unlockedtocraft': 'false',
     'unlockedtoequip': 'false',
     'weight': '3'}

    In [31]: ri.getchildren()
    Out[31]: 
    [<Element 'projectile' at 0x7fd2afa6b728>,
     <Element 'SocketPreset' at 0x7fd2afa6b818>,
     <Element 'craftingrequirements' at 0x7fd2afa6b868>,
     <Element 'craftingspelllist' at 0x7fd2afa6b908>,
     <Element 'AudioInfo' at 0x7fd2afa6bb88>]

    In [32]: ri.get('projectile')

    In [33]: ri.find('projectile')
    Out[33]: <Element 'projectile' at 0x7fd2afa6b728>

    In [34]: ri.find('craftingrequirements')
    Out[34]: <Element 'craftingrequirements' at 0x7fd2afa6b868>

    In [35]: c = _

    In [36]: c
    Out[36]: <Element 'craftingrequirements' at 0x7fd2afa6b868>

    In [37]: c.getchildren()
    Out[37]: [<Element 'craftresource' at 0x7fd2afa6b8b8>]

    In [38]: c.getchildren()[0]
    Out[38]: <Element 'craftresource' at 0x7fd2afa6b8b8>

    In [39]: c.getchildren()[0].attrib
    Out[39]: {'count': '32', 'uniquename': 'T2_PLANKS'}

    """


def build_localization_lookup(lang='EN-US'):
    """
    Takes the localization XML and builds a lookup dictionary for the language given
    :return: dictionary of {itemID:localized name}
    """
    loc_dict = {}

    loc_tree = ET.parse('libs/game_data/localization.xml')
    loc_root = loc_tree.getroot()

    # TODO: This [0] reference might cause a bug, find a cleaner way
    loc_items = loc_root.getchildren()[0]

    for item in loc_items:
        try:
            # Get the item ID string
            item_id = item.attrib['tuid']

            # Get the target lang for localization
            for loc_str in item:
                if loc_str.attrib['{http://www.w3.org/XML/1998/namespace}lang'] == lang:
                    localized = loc_str.find('seg').text

                    if localized is not None:
                        loc_dict[item_id] = localized
                    else:
                        loc_dict[item_id] = item_id
                    break
                else:
                    loc_dict[item_id] = item_id

        except:
            print(traceback.format_exc())

    return loc_dict


def get_crafting_requirements():
    """
    Returns what items are required for crafting the given ITEM ID
    :return:
    """
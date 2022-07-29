from pyppeteer import launch
from pyppeteer_stealth import stealth
from typing import Tuple
import requests
import json
import os
from env_logger import EnvLogger

class Tracker:
    def __init__( self, cronos_api_key = None ) -> None:
        if cronos_api_key is None:
            raise ValueError( 'You need to set up cronos api-key.' )
        self.__cronos_api_key = cronos_api_key
        self.__headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36' }
        self.__erc721_floor_price_cls = '.sc-4388aed4-1.fyzfJG'
        self.__erc1155_floor_price_cls = '.fs-3.ms-1'
        self.__logger = EnvLogger( 'Tracker.cls' )
    # __init__()

    def __is_erc1155( self, url ) -> Tuple[str, str]:
        ''' 
        Check eb url is a erc1155 collection. 
        return ( type, new_url )
        '''
        if 'vip-founding-member' in url:
            return ( '1155', f'{url}/2' )
        elif 'founding-member' in url:
            return ( '1155', f'{url}/1' )
        elif 'lost-toys-vip' in url:
            return ( '1155', f'{url}/1' )
        else:
            return ( '721', url )
    # __is_erc1155()
    
    async def track_floor( self, url:str ) -> Tuple[str, str]:
        '''
        Using url to get token type and floor price of the collection on Ebisu's bay.\n
        return ( erc_type, price )
        '''
        browser = await launch( headless = True,
                                executablePath = f'{os.getcwd()}\chromium\chrome.exe',
                                args = ['--start-maximized', '--no-sandbox', '--disable-infobars'] )
        page = await browser.newPage()
        await page.evaluateOnNewDocument( 'delete navigator.__proto__.webdriver ;' )
        await page.setUserAgent( 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                 'Chrome/98.0.4758.102 Safari/537.36' )
        await stealth( page )

        ( erc_type, url ) = self.__is_erc1155( url )

        try:
            await page.goto( url, options = {'timeout': 5000} )

            if erc_type == '721':
                element = await page.waitForSelector( self.__erc721_floor_price_cls, timeout = 6000 )
            else:
                element = await page.waitForSelector( self.__erc1155_floor_price_cls, timeout = 6000 )

            floor_price = await ( await element.getProperty( 'textContent' )).jsonValue()
            floor_price = floor_price.replace( ' CRO', '' )

            await browser.close()
            return ( erc_type, floor_price )
        # try

        except Exception as e:
            self.__logger.error( e )
            await browser.close()
            return ( '', '' )
        # except
    # track_floor()

    async def track_with_detail( self, erc_type:str, url:str ) -> Tuple[str, str]:
        '''
        Using url to get floor price of the collections with detail info.(screenshot) on Ebisu's bay.\n
        There are no detail info. for erc1155 token, only floor price is actual value.
        return ( screenshot path, floor price )
        '''

        browser = await launch( headless = True,
                                #defaultViewport = None,
                                executablePath = f'{os.getcwd()}\chromium\chrome.exe',
                                args = ['--start-maximized', '--no-sandbox', '--disable-infobars'] )
        page = await browser.newPage()
        await page.setViewport( {'width': 1720, 'height': 1350} )
        await page.evaluateOnNewDocument( 'delete navigator.__proto__.webdriver ;' )
        await page.setUserAgent( 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                 'Chrome/98.0.4758.102 Safari/537.36' )
        await stealth( page )
        
        try:                               
            if erc_type == '721':
                await page.goto( url, options = {'timeout': 6000} ) 
                element = await page.waitForSelector( self.__erc721_floor_price_cls, timeout = 6000 )
                floor_price = await ( await element.getProperty( 'textContent' )).jsonValue()
                floor_price = floor_price.replace( ' CRO', '' )

                # Not work in headless mode
                # await element.hover()
                series = url.replace( 'https://app.ebisusbay.com/collection/', '' )
                await page.screenshot( { 'path': f'screenshot/{series}.png', 'fullPage': False} )
                await browser.close()
                return ( f'screenshot/{series}.png', floor_price )
            # if
            else: # for now is '1155'
                ( erc_type, url ) = self.__is_erc1155( url )

                await page.goto( url, options = {'timeout': 6000} ) 
                element = await page.waitForSelector( self.__erc1155_floor_price_cls, timeout = 6000 )
                floor_price = await ( await element.getProperty( 'textContent' )).jsonValue()
                floor_price = floor_price.replace( ' CRO', '' )
                await browser.close()
                return ( '', floor_price )
            # else
            
        # try

        except Exception as e:
            self.__logger.error( e )
            await browser.close()
            return ( '', '' )
        # except
    # track_with_rank()

    def cronos_api_status( self ) -> bool:
        '''
        Check api status, if work return True.
        return status
        '''
        url = ( f'https://api.cronoscan.com/api?module=stats&action=supply&apikey={self.__cronos_api_key}' )

        try:
            response = requests.get( url, headers = self.__headers, timeout = 5 )
            result = ( json.loads( response.text ) ).get( 'message' )
            return ( result == 'OK' )
        # try
        except Exception as e:
            self.__logger.error( e )
            return False
        # except
    # cronos_api_status()

    def current_token_supply( self, contrats_addr:str ) -> str:
        '''
        using a contract address to get the collection total supply.\n
        return ( total supply )
        '''
        url = ( 'https://api.cronoscan.com/api?module=stats&action=tokensupply&' +
                f'contractaddress={contrats_addr}&apikey={self.__cronos_api_key}' )
        
        try:
            response = requests.get( url, headers = self.__headers, timeout = 5 )
            result = ( json.loads( response.text ) ).get( 'result' )
            return result
        # try
        except Exception as e:
            self.__logger.error( e )
            return ''
        # except
    # current_token_supply()

# class Tracker

from msilib.schema import Error
from requests import Session
import json
import math
from env_logger import EnvLogger

class CMCFunction():
    def __init__( self, api_key:str = None ) -> None:
        if api_key is None:
            raise Error( 'CMC API KEY is required!' )
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key
        }

        self.__session = Session()
        self.__session.headers.update( headers )
        self.__logger = EnvLogger( 'CMCFunction.cls' )
    # __init__()

    def usd_to_cro( self ) -> float:
        ''' Get latest CRO value in USD. '''
        try:
            url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
            params = {
                'amount': 1,
                'symbol': 'USD',
                'convert': 'CRO'
            }
            response = self.__session.get( url, params = params )
            data = json.loads(response.text)
            price = data.get( 'data' )[0].get( 'quote' ).get( 'CRO' ).get( 'price' )

            return price
        # try
        except Exception as e:
            self.__logger.error( f'無法從 CMC API 獲取最新價格資訊: {e}' )
            return -1
        # except
    # usd_to_cro()

    def cro_to_usd( self ) -> float:
        ''' Get latest USD value in CRO. '''
        try:
            url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
            params = {
                'amount': 1,
                'symbol': 'CRO',
                'convert': 'USD'
            }
            response = self.__session.get( url, params = params )
            data = json.loads(response.text)
            price = data.get( 'data' )[0].get( 'quote' ).get( 'USD' ).get( 'price' )
            price = math.floor( price * 1000000 ) / 1000000.0 # USD Decimal is 6

            return price
        # try
        except Exception as e:
            self.__logger.error( f'無法從 CMC API 獲取最新價格資訊: {e}' )
            return -1
        # except
    # cro_to_usd()
        
# class CMCFunction

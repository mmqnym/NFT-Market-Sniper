
import json
from typing import Tuple

class Configs:
    __instance = None

    def __new__( cls, *args, **kwargs ): 
        if cls.__instance is None: 
            cls.__instance = super().__new__( cls )
        
        return cls.__instance
    # __new__()

    def __init__( self ) -> None:
        self.__configs = {}
    # __init__()

    def init( self ) -> Tuple[bool, str]:
        ''' 
        Initialize configs from configs.json.\n
        return ( status, reason )
        '''
        try:
            with open( 'settings.json', 'r', encoding = 'utf-8' ) as f:
                self.__configs = json.load( f )
            
            ok, loss_var = self.__check_data_integrity()

            if ( ok ):
                return ( True, '' )
            return ( False, f'發生讀取遺失參數例外: {loss_var}' )
        # try
        except Exception as e:
            return ( False, f'讀取 configs 失敗: {e}' )
    # init()

    def __check_data_integrity( self ) -> Tuple[bool, str]:
        ''' 
        Check data is complete after read.
        return ( ok, description of first find a loss variable )
        '''
        try:
            self.get_bot_token()
            self.get_owner_id()
            self.get_system_log_channel()
            self.get_floor_tracker_channel()
            self.get_mint_tracker_channel()
            self.get_cronoscan_api_key()
            self.get_cmc_api_key()
            self.get_done_img_url()
            self.get_error_img_url()
            self.get_choose_img_url()
            self.get_hello_and_bye_img_url()
            self.get_floor_change_img_url()
            return ( True, '' )

        except Exception as e:
            return ( False, e )
    # __check_data_integrity()

    def __update( self ) -> Tuple[bool, str]:
        '''
        Write new configs to configs.json when configs is changed.\n
        return ( status, reason )
        '''

        try:
            with open( r'settings.json', 'w', encoding = 'utf-8' ) as f:
                json.dump( self.__configs, f, ensure_ascii = False, indent = 4 )
                
            return ( True, '' )

        except Exception as e:
            return ( False, f'更新 configs 失敗: {e}' )
    # __update()

    def set_system_log_channel( self, channel:str ) -> Tuple[bool, str]:
        '''
        Set channel for system log.\n
        return ( status, reason )
        '''
        
        rollback = self.__configs.get( 'SYSTEM_LOG_CHANNEL_ID' )
        self.__configs['SYSTEM_LOG_CHANNEL_ID'] = channel
        ( status, reason ) = self.__update()

        if not status:
            self.__configs['SYSTEM_LOG_CHANNEL_ID'] = rollback

        return ( status, reason )
    # set_system_log_channel()

    def get_system_log_channel( self ) -> str:
        return self.__configs.get( 'SYSTEM_LOG_CHANNEL_ID' )
    # get_system_log_channel()

    def set_floor_tracker_channel( self, channel:str ) -> Tuple[bool, str]:
        '''
        Set channel for sending floor price infomation.\n
        return ( status, reason )
        '''

        rollback = self.__configs.get( 'FLOOR_TRACKER_CHANNEL_ID' )
        self.__configs['FLOOR_TRACKER_CHANNEL_ID'] = channel
        ( status, reason ) = self.__update()

        if not status:
            self.__configs['FLOOR_TRACKER_CHANNEL_ID'] = rollback

        return ( status, reason )
    # set_floor_tracker_channel()

    def get_floor_tracker_channel( self ) -> str:
        ''' return binded floor price tracker channel '''
        return self.__configs.get( 'FLOOR_TRACKER_CHANNEL_ID' )
    # get_floor_tracker_channel()

    def set_mint_tracker_channel( self, channel:str ) -> Tuple[bool, str]:
        '''
        Set channel for sending mint infomation. ( current total supply )\n
        return ( status, reason )
        '''

        rollback = self.__configs.get( 'MINT_TRACKER_CHANNEL_ID' )
        self.__configs['MINT_TRACKER_CHANNEL_ID'] = channel
        ( status, reason ) = self.__update()

        if not status:
            self.__configs['MINT_TRACKER_CHANNEL_ID'] = rollback

        return ( status, reason )
    # set_mint_tracker_channel()

    def get_mint_tracker_channel( self ) -> str:
        return self.__configs.get( 'MINT_TRACKER_CHANNEL_ID' )
    # get_mint_tracker_channel()

    def get_bot_token( self ) -> str:
        return self.__configs.get( 'BOT_TOKEN' )
    # get_bot_token()

    def get_owner_id( self ) -> str:
        return self.__configs.get( 'OWNER_ID' )
    # get_owner_id()

    def get_cronoscan_api_key( self ) -> str:
        return self.__configs.get( 'CRONOSCAN_API_KEY' )
    # get_bot_token()

    def get_cmc_api_key( self ) -> str:
        return self.__configs.get( 'COINMARKETCAP_API_KEY' )
    # get_cmc_api_key()

    def get_hello_and_bye_img_url( self ) -> str:
        return self.__configs.get( 'HELLO_AND_BYE_IMG_URL' )
    # get_hello_and_bye_img_url()

    def get_done_img_url( self ) -> str:
        return self.__configs.get( 'DONE_IMG_URL' )
    # get_done_img_url()

    def get_choose_img_url( self ) -> str:
        return self.__configs.get( 'CHOOSE_IMG_URL' )
    # get_choose_img_url()

    def get_error_img_url( self ) -> str:
        return self.__configs.get( 'ERROR_IMG_URL' )
    # get_error_img_url()

    def get_floor_change_img_url( self ) -> str:
        return self.__configs.get( 'FLOOR_CHANGE_IMG_URL' )
    # get_floor_change_img_url()

    def get_fishing_img_url( self ) -> str:
        return self.__configs.get( 'FISHING_IMG_URL' )
    # get_fishing_img_url()
# class Configs

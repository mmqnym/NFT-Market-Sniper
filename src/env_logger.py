import logging

class EnvLogger:
    def __init__( self, name:str, level:str = 'debug' ) -> None:
        self.__env_logger: logging.Logger = logging.getLogger( name = name )

        if level.lower() == 'debug':
            self.__env_logger.setLevel( logging.DEBUG )
        elif level.lower() == 'info':
            self.__env_logger.setLevel( logging.INFO )
        elif level.lower() == 'warning':
            self.__env_logger.setLevel( logging.WARNING )
        elif level.lower() == 'error':
            self.__env_logger.setLevel( logging.ERROR )
        elif level.lower() == 'critical':
            self.__env_logger.setLevel( logging.CRITICAL )
        else:
            self.__env_logger.setLevel( logging.DEBUG )

        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: logging.Formatter = logging.Formatter( '[%(levelname)s] %(module)s.%(funcName)s ' + 
                                                          'says: {%(message)s} ...%(asctime)s' )
        handler.setFormatter( formatter )
        self.__env_logger.addHandler( handler )
    # __init__()

    def debug( self, log:str ):
        self.__env_logger.debug( log )
    
    def info( self, log:str ):
        self.__env_logger.info( log )

    def warning( self, log:str ):
        self.__env_logger.warning( log )

    def error( self, log:str ):
        self.__env_logger.error( log )

    def critical( self, log:str ):
        self.__env_logger.critical( log )

# class EnvLogger
